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
    total_length = sum(len(word) for word in language)  # Calcul de la longueur totale des mots dans le langage
    probabilities = {}  # Dictionnaire pour stocker les probabilités de chaque chiffre (0 ou 1)
    for word in language:
        for digit in word:
            probabilities[digit] = probabilities.get(digit, 0) + 1
    for digit in probabilities:
        probabilities[digit] /= total_length
    entropy_value = -sum(prob * log2(prob) for prob in probabilities.values())
    
    return entropy_value

def generer_mot_binaire():
    longueur = random.randint(1,7) 
    mot = ''.join(random.choice(['0', '1']) for _ in range(longueur))
    return mot

def generer_langage():
    nombre_de_mots = random.randint(1, 10)
    langage = {generer_mot_binaire() for _ in range(nombre_de_mots)}
    return list(langage)

mot_binaire = generer_mot_binaire()
langage = generer_langage()

result = []
for i in range(5000):
    dic = {
        '01': 0,
        '10': 0,
        '11': 0,
        '00': 0,
        '000': 0,
        '001': 0,
        '010': 0,
        '011': 0,
        '100': 0,
        '101': 0,
        '110': 0,
        '111': 0,
        'nombre':0,
        'code': 0
        }

    l = generer_langage()    
    print(l)
    print(est_un_code(l),"\n")

    dic['code'] = est_un_code(l)
    dic['nombre'] = len(l)
    for word in l:
        for pattern in dic:
            if word.endswith(pattern):
                dic[pattern] += 1
    result.append(dic)

with open('resultats.csv', mode='w', newline='') as fichier_csv:
    writer = csv.writer(fichier_csv)
    writer.writerow(dic.keys())
    for lang in result:
        writer.writerow(lang.values())