from flask import Flask, jsonify

app = Flask(__name__)

# Adresse du serveur "Hello World"
SERVER_URL = "localhost:3001"

@app.route("/getServer", methods=["GET"])
def get_server():
    return jsonify({"code": 200, "server": SERVER_URL})

if __name__ == "__main__":
    app.run(port=4000, debug=True)
