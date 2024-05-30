from flask import Flask, request, render_template, jsonify
import pandas as pd
import joblib
from math import log2

app = Flask(__name__)

modele_charge = joblib.load('./models.pkl')
historique = []  # Liste pour stocker l'historique des prédictions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_string = request.form.get('input_string')
    try:
        l = [x.strip() for x in input_string.split(',')]

        dic = {
            'prefix': int(with_prefix(l)),
            'code': int(est_un_code(l)),
            'nombre': int(len(l)),
            'longueur_moyenne': float(longueur_moyenne(l)),
            'profondeur_maximale': float(profondeur_maximale(l)),
            'variance_longueur': float(variance_longueur(l)),
            'balancedness': float(balancedness(l)),
            '00_ngrams': int(n_grams(l, 2)),
            '11_ngrams': int(n_grams(l, 2))
        }

        data = pd.DataFrame([dic], columns=['prefix', 'longueur_moyenne', 'profondeur_maximale', 'variance_longueur', 'balancedness', '00_ngrams', '11_ngrams', 'nombre'])
        predictions = modele_charge.predict(data)

        response = {
            'l': l,
            'prediction': int(predictions[0]),
            'real_result': int(est_un_code([item.replace("'", "").strip() for item in l]))
        }

        # Ajouter la prédiction à l'historique
        historique.append(response)

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/history', methods=['GET'])
def history():
    return jsonify(historique)

def prefix(l, p):
    result = []
    for pref in p:
        for mot in l:
            if pref == mot[:len(pref)]:
                suffix = mot[len(pref):]
                if suffix:
                    result.append(suffix)
    return result

def sardinas(l):
    l1 = prefix(l, l)
    result = [l1]
    a = 5
    while a > 1:
        last_set = result[-1]
        one = prefix(last_set, l)
        two = prefix(l, last_set)
        ensemble = one + two
        if not ensemble:
            return result, 0
        if any(word in l for word in ensemble):
            return result, 1
        result.append(ensemble)
        a -= 1
    return result, 1

def est_un_code(l):
    _, is_code = sardinas(l)
    return is_code

def entropy(language):
    total_length = sum(len(word) for word in language)
    probabilities = {}
    for word in language:
        for digit in word:
            probabilities[digit] = probabilities.get(digit, 0) + 1
    for digit in probabilities:
        probabilities[digit] /= total_length
    entropy_value = -sum(prob * log2(prob) for prob in probabilities.values())
    return round(entropy_value, 2)

def longueur_moyenne(language):
    return round(sum(len(word) for word in language) / len(language), 2) if language else 0

def profondeur_maximale(language):
    return round(max(len(word) for word in language), 2) if language else 0

def variance_longueur(language):
    moy = longueur_moyenne(language)
    return round(sum((len(word) - moy) ** 2 for word in language) / len(language), 2) if language else 0

def balancedness(language):
    min_length = min(len(word) for word in language) if language else 0
    max_length = profondeur_maximale(language)
    return round(max_length - min_length, 2)

def n_grams(language, n):
    ngram_count = 0
    for word in language:
        if len(word) >= n:
            ngram_count += word.count('0' * n) + word.count('1' * n)
    return ngram_count

def with_prefix(language):
    count = 0
    for prefix in language:
        for word in language:
            if word.startswith(prefix):
                count += 1
    return round(count / len(language))

if __name__ == '__main__':
    app.run(debug=True)
