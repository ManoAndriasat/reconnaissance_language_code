
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier


column_names = {
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

data = pd.read_csv("resultats.csv", names=column_names, skiprows=1)

X = data.drop('code', axis=1)
y = data['code']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

tree_clf = GradientBoostingClassifier()

tree_clf.fit(X_train, y_train)
y_pred = tree_clf.predict(X_test)
cm = confusion_matrix(y_test, y_pred)

accuracy = accuracy_score(y_test, y_pred)
print("Exactitude de l'arbre de décision :", accuracy*100 , "%")

joblib.dump(tree_clf, 'models.pkl')

