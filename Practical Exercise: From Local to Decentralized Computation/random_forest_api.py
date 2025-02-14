from flask import Flask, request, jsonify
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import numpy as np

# Charger le dataset Iris
iris = datasets.load_iris()
X, y = iris.data, iris.target  # Features et labels

# Séparer en train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalisation des données
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Entraîner les modèles
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Initialisation de Flask
app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def predict():
    try:
        # Récupérer les paramètres
        features = np.array([[
            float(request.args.get('sepal_length')),
            float(request.args.get('sepal_width')),
            float(request.args.get('petal_length')),
            float(request.args.get('petal_width'))
        ]])

        # Normaliser
        features = scaler.transform(features)

        # Prédictions
        pred_rf = rf.predict(features)[0]

        return jsonify({
            "status": "success",
            "predictions": {
                "RandomForest": iris.target_names[pred_rf]
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
