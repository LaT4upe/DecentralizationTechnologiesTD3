from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]

# Collections
products_collection = db["products"]
orders_collection = db["orders"]
cart_collection = db["cart"]

print("Base de données MongoDB prête !")
