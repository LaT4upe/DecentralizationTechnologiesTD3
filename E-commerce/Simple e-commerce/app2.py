from flask import Flask
from database import products_collection, orders_collection, cart_collection

app = Flask(__name__)

@app.route("/")
def home():
    return "E-commerce API is running!"

if __name__ == "__main__":
    app.run(debug=True)
