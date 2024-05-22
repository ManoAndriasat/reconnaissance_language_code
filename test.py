import pandas as pd
import joblib

# Fonction pour obtenir les suffixes après avoir supprimé les préfixes
def prefix(l, p):
    result = []
    for pref in p:
        for mot in l:
            if pref == mot[:len(pref)]:
                suffix = mot[len(pref):]
                if suffix:
                    result.append(suffix)
    return result

# Implémentation de l'algorithme de Sardinas-Patterson
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

# Fonction pour vérifier si l'ensemble est un code
def est_un_code(l):
    _, is_code = sardinas(l)
    return is_code

# Chargement du modèle sauvegardé
modele_charge = joblib.load('./models.pkl')

# Initialisation du dictionnaire avec les combinaisons à vérifier
dic = {
    '01': 0, '10': 0, '11': 0, '00': 0,
    '000': 0, '001': 0, '010': 0, '011': 0,
    '100': 0, '101': 0, '110': 0, '111': 0,
    'nombre': 0
}

# Liste de chaînes de bits
l = ['011011', '00', '101', '110000']

# Mise à jour du nombre total d'éléments dans la liste
dic['nombre'] = len(l)

# Boucle pour vérifier chaque chaîne dans la liste
for mot in l:
    # Vérification des occurrences de chaque combinaison de deux bits
    dic['01'] += mot.count('01')
    dic['10'] += mot.count('10')
    dic['11'] += mot.count('11')
    dic['00'] += mot.count('00')
    
    # Vérification des occurrences de chaque combinaison de trois bits
    dic['000'] += mot.count('000')
    dic['001'] += mot.count('001')
    dic['010'] += mot.count('010')
    dic['011'] += mot.count('011')
    dic['100'] += mot.count('100')
    dic['101'] += mot.count('101')
    dic['110'] += mot.count('110')
    dic['111'] += mot.count('111')

# Préparation des résultats pour la prédiction
result = [dic[key] for key in ['01', '10', '11', '00', '000', '001', '010', '011', '100', '101', '110', '111', 'nombre']]
data = pd.DataFrame([result], columns=['01', '10', '11', '00', '000', '001', '010', '011', '100', '101', '110', '111', 'nombre'])

print(data)

# Faire des prédictions avec le modèle chargé
predictions = modele_charge.predict(data)
print("Prédictions pour les nouvelles données:")
print(predictions)
