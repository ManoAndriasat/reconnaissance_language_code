import pandas as pd
import joblib
from math import log2
import tkinter as tk
from tkinter import messagebox

history = []
def on_predict_button_click():
    input_string = input_entry.get()
    
    try:
        l = input_string.split(',')
        
        dic['prefix'] = with_prefix(l)
        dic['code'] = est_un_code(l)
        dic['nombre'] = len(l)
        dic['longueur_moyenne'] = longueur_moyenne(l)
        dic['entropie'] = entropy(l)
        dic['profondeur_maximale'] = profondeur_maximale(l)
        dic['variance_longueur'] = variance_longueur(l)
        dic['balancedness'] = balancedness(l)
        dic['00_ngrams'] = n_grams(l, 2)
        dic['11_ngrams'] = n_grams(l, 2)
        
        result = [dic[key] for key in ['prefix', 'longueur_moyenne', 'entropie', 'profondeur_maximale', 'variance_longueur', 'balancedness', '00_ngrams', '11_ngrams', 'nombre']]
        data = pd.DataFrame([dic], columns=['prefix', 'longueur_moyenne', 'entropie', 'profondeur_maximale', 'variance_longueur', 'balancedness', '00_ngrams', '11_ngrams', 'nombre'])
        
        predictions = modele_charge.predict(data)
        
        
        sardinas_label.config(text=f"Prediction: {predictions[0]}")
        l = [item.replace("'","").strip() for item in l]
        prediction_label.config(text=f"vrai resultat: {est_un_code(l)}")
        history.append({'l':l,'prediction':predictions[0],'reel':est_un_code(l)})

        label = tk.Label(window, text=history[0], height=2, width=80)
        label.pack()
        history.pop()
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to predict: {str(e)}")


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

def generer_mot_binaire():
    longueur = random.randint(1,7)
    mot = ''.join(random.choice(['0', '1']) for _ in range(longueur))
    return mot

def generer_langage():
    nombre_de_mots = random.randint(1, 10)
    langage = {generer_mot_binaire() for _ in range(nombre_de_mots)}
    return list(langage)

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
    return round(count/len(language))


modele_charge = joblib.load('./models.pkl')
dic = {
    'prefix':0,
    'longueur_moyenne': 0,
    'entropie': 0,
    'profondeur_maximale': 0,
    'variance_longueur': 0,
    'balancedness': 0,
    '00_ngrams': 0,
    '11_ngrams': 0,
    'nombre': 0,
    'code': 0
}
l = ['101000', '0010', '101', '01011', '0011000', '0110', '011', '1110']

dic['prefix'] = with_prefix(l)
dic['code'] = est_un_code(l)
dic['nombre'] = len(l)
dic['longueur_moyenne'] = longueur_moyenne(l)
dic['entropie'] = entropy(l)
dic['profondeur_maximale'] = profondeur_maximale(l)
dic['variance_longueur'] = variance_longueur(l)
dic['balancedness'] = balancedness(l)
dic['00_ngrams'] = n_grams(l, 2)
dic['11_ngrams'] = n_grams(l, 2)

result = [dic[key] for key in ['prefix', 'longueur_moyenne', 'entropie', 'profondeur_maximale', 'variance_longueur', 'balancedness', '00_ngrams', '11_ngrams', 'nombre']]
data = pd.DataFrame([dic],columns=['prefix', 'longueur_moyenne', 'entropie', 'profondeur_maximale', 'variance_longueur', 'balancedness', '00_ngrams', '11_ngrams', 'nombre'])

print(data)

predictions = modele_charge.predict(data)
print(predictions)


# Create the main window
window = tk.Tk()
window.title("Machine Learning Prediction")
window.configure(bg='#FFFFFF')  # Set background color

# Frame for inputs and buttons
input_frame = tk.Frame(window, bg='#E0E0E0')
input_frame.pack(padx=20, pady=(20, 10))

# Entry widget for input
input_entry = tk.Entry(input_frame, width=50, font=('Arial', 14))
input_entry.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

# Button to trigger prediction
predict_button = tk.Button(input_frame, text="Predict", font=('Arial', 14), command=on_predict_button_click)
predict_button.grid(row=0, column=1, padx=10, pady=10)

# Frame for labels
label_frame = tk.Frame(window, bg='#E0E0E0')
label_frame.pack(padx=20, pady=(10, 20))

# Label to display the prediction result
prediction_label = tk.Label(label_frame, text="", font=('Arial', 16), wraplength=400, justify='center')
prediction_label.grid(row=0, column=0, padx=10, pady=10)
# Label to display the prediction result
prediction_label = tk.Label(label_frame, text="", font=('Arial', 16), wraplength=400, justify='center')
prediction_label.grid(row=0, column=0, padx=10, pady=10)

# Sardinas label
sardinas_label = tk.Label(label_frame, text="", font=('Arial', 16), wraplength=400, justify='center')
sardinas_label.grid(row=1, column=0, padx=10, pady=10)

# Run the Tkinter event loop
window.mainloop()