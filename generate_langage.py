import random
import csv
from math import log2

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

result = []
for i in range(5000):
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

    l = generer_langage()
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
    

    result.append(dic)
    l.append(est_un_code(l))
    print(l)

with open('resultats.csv', mode='w', newline='') as fichier_csv:
    writer = csv.writer(fichier_csv)
    writer.writerow(dic.keys())
    for lang in result:
        writer.writerow(lang.values())
