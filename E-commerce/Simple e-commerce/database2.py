from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Modèle pour les produits
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

# Modèle pour les commandes
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    products = db.Column(db.String(500), nullable=False)  # Stocker sous forme JSON
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="pending")

# Modèle pour le panier
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    products = db.Column(db.String(500), nullable=False)  # Stocker sous forme JSON
    total_price = db.Column(db.Float, nullable=False)

# Créer la base de données
with app.app_context():
    db.create_all()

print("Base de données initialisée !")
