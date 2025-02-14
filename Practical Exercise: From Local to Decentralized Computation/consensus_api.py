from flask import Flask, request, jsonify
import requests
import numpy as np

# URLs des APIs de chaque membre (remplace avec vos vraies URLs ngrok)
API_ENDPOINTS = [
    "https://knn123.ngrok.io/predict",  # API du membre 1 (KNN)
    "https://rf456.ngrok.io/predict",  # API du membre 2 (RandomForest)
    "https://lr789.ngrok.io/predict"   # API du membre 3 (LogisticRegression)
]

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
        predictions = []
        for url in API_ENDPOINTS:
            try:
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    pred = response.json()["prediction"]
                    predictions.append(pred)
            except Exception as e:
                print(f"Erreur avec {url}: {e}")
                continue

        if not predictions:
            return jsonify({"status": "error", "message": "Aucune prédiction reçue"}), 500

        # Calcul du consensus (majorité)
        final_prediction = max(set(predictions), key=predictions.count)

        return jsonify({
            "status": "success",
            "individual_predictions": predictions,
            "consensus_prediction": final_prediction
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)
