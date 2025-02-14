from flask import Flask, request, jsonify
import requests
import numpy as np

# URLs des APIs ngrok

# KNN = https://4a9a-77-196-229-19.ngrok-free.app/
# RF = https://beda-83-204-229-229.ngrok-free.app/
# LR = https://a740-2a01-cb00-167a-3300-a9dc-c0b1-b583-17bf.ngrok-free.app/


API_ENDPOINTS = [
    "https://4a9a-77-196-229-19.ngrok-free.app/predict",  # API KNN
    "https://beda-83-204-229-229.ngrok-free.app/predict",  # API RandomForest
    "https://a740-2a01-cb00-167a-3300-a9dc-c0b1-b583-17bf.ngrok-free.app/predict"   # API LogisticRegression
]

# Poids fixes attribués
MODEL_WEIGHTS = {
    "https://4a9a-77-196-229-19.ngrok-free.app/predict": 0.3,  # KNN
    "https://beda-83-204-229-229.ngrok-free.app/predict": 0.5,  # Random Forest
    "https://a740-2a01-cb00-167a-3300-a9dc-c0b1-b583-17bf.ngrok-free.ap/predict": 0.2   # Logistic Regression
}

app = Flask(__name__)

@app.route('/consensus', methods=['GET'])
def consensus():
    try:
        # Récupérer les paramètres
        params = {
            "sepal_length": request.args.get("sepal_length"),
            "sepal_width": request.args.get("sepal_width"),
            "petal_length": request.args.get("petal_length"),
            "petal_width": request.args.get("petal_width")
        }

        # Récupérer les prédictions de chaque API
        predictions = {}
        for url in API_ENDPOINTS:
            try:
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    pred_json = response.json()
                    if "predictions" in pred_json:
                        # Extraire la valeur correcte selon le modèle
                        for model_name in ["KNN", "RandomForest", "LogisticRegression"]:
                            if model_name in pred_json["predictions"]:
                                predictions[url] = pred_json["predictions"][model_name]
            except Exception as e:
                print(f"Erreur avec {url}: {e}")
                continue

        if not predictions:
            return jsonify({"status": "error", "message": "Aucune prédiction reçue"}), 500

        # Calcul du consensus pondéré
        weighted_votes = {}
        for url, pred in predictions.items():
            weighted_votes[pred] = weighted_votes.get(pred, 0) + MODEL_WEIGHTS.get(url, 0)
        consensus_prediction = max(weighted_votes, key=weighted_votes.get)

        return jsonify({
            "status": "success",
            "individual_predictions": predictions,
            "model_weights": MODEL_WEIGHTS,
            "consensus_prediction": consensus_prediction
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Ce serveur tourne sur un port différent
