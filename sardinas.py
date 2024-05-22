import random

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


l = ['011','11','00','101','011','0011']    

print("Les ensembles générés par l'algorithme de Sardinas-Patterson :", sardinas(l))
print("Est-ce que l'ensemble est un code préfixe ? ", est_un_code(l))
