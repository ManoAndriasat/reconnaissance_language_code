
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix


column_names ={
    '01': 0, '10': 0, '11': 0, '00': 0,
    '000': 0, '001': 0, '010': 0, '011': 0,
    '100': 0, '101': 0, '110': 0, '111': 0,
    'nombre': 0,
    'code': 0}
data = pd.read_csv("resultats.csv", names=column_names, skiprows=1)

X = data.drop('code', axis=1)
y = data['code']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

tree_clf = DecisionTreeClassifier()

tree_clf.fit(X_train, y_train)

# Faire des prédictions sur l'ensemble de test
y_pred = tree_clf.predict(X_test)

# Calculer la matrice de confusion
cm = confusion_matrix(y_test, y_pred)

accuracy = accuracy_score(y_test, y_pred)
print("Exactitude de l'arbre de décision :", accuracy*100 , "%")

joblib.dump(tree_clf, 'models.pkl')

