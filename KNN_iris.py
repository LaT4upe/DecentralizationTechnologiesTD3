from flask import Flask, request, jsonify
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# Charger le dataset Iris
iris = datasets.load_iris()
X, y = iris.data, iris.target  # Features et labels

# Séparer en train/test (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalisation des données
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Création et entraînement du modèle KNN
k = 5  # Nombre de voisins
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(X_train, y_train)

# Initialisation de Flask
app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def predict():
    try:
        # Récupérer les paramètres depuis la requête GET
        sepal_length = float(request.args.get('sepal_length'))
        sepal_width = float(request.args.get('sepal_width'))
        petal_length = float(request.args.get('petal_length'))
        petal_width = float(request.args.get('petal_width'))

        # Créer un tableau numpy avec les données
        features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

        # Normaliser les données
        features = scaler.transform(features)

        # Faire la prédiction
        prediction = knn.predict(features)
        predicted_class = iris.target_names[prediction[0]]

        # Retourner la réponse JSON
        return jsonify({"prediction": predicted_class})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
