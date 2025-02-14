from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permet d'éviter les erreurs CORS si un front JS est utilisé.

# Connexion à MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/ecommerce"
mongo = PyMongo(app)

# Collections
products_collection = mongo.db.products
orders_collection = mongo.db.orders
cart_collection = mongo.db.cart


# ------------------ ROUTES PRODUITS ------------------

@app.route('/products', methods=['GET'])
def get_products():
    """ Récupère tous les produits avec filtres facultatifs """
    category = request.args.get("category")
    in_stock = request.args.get("inStock")

    query = {}
    if category:
        query["category"] = category
    if in_stock is not None:
        query["stock"] = {"$gt": 0} if in_stock.lower() == "true" else 0

    products = list(products_collection.find(query))
    for product in products:
        product["_id"] = str(product["_id"])  # Convertir ObjectId en string

    return jsonify(products)


@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """ Récupère un produit spécifique par ID """
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        return jsonify({"error": "Produit introuvable"}), 404

    product["_id"] = str(product["_id"])
    return jsonify(product)


@app.route('/products', methods=['POST'])
def add_product():
    """ Ajoute un nouveau produit """
    data = request.json
    if not all(k in data for k in ("name", "description", "price", "category", "stock")):
        return jsonify({"error": "Données invalides"}), 400

    new_product = {
        "name": data["name"],
        "description": data["description"],
        "price": data["price"],
        "category": data["category"],
        "stock": data["stock"]
    }
    product_id = products_collection.insert_one(new_product).inserted_id
    return jsonify({"message": "Produit ajouté", "id": str(product_id)}), 201


@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """ Met à jour un produit """
    data = request.json
    updated_product = {k: v for k, v in data.items() if k in ("name", "description", "price", "category", "stock")}

    result = products_collection.update_one({"_id": ObjectId(product_id)}, {"$set": updated_product})
    if result.matched_count == 0:
        return jsonify({"error": "Produit introuvable"}), 404

    return jsonify({"message": "Produit mis à jour"})


@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """ Supprime un produit """
    result = products_collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Produit introuvable"}), 404

    return jsonify({"message": "Produit supprimé"})


# ------------------ ROUTES COMMANDES ------------------

@app.route('/orders', methods=['POST'])
def create_order():
    """ Crée une nouvelle commande """
    data = request.json
    if "products" not in data or not isinstance(data["products"], list):
        return jsonify({"error": "Données invalides"}), 400

    total_price = 0
    order_items = []

    for item in data["products"]:
        product = products_collection.find_one({"_id": ObjectId(item["product_id"])})
        if not product or product["stock"] < item["quantity"]:
            return jsonify({"error": "Stock insuffisant ou produit introuvable"}), 400

        # Calcul du prix total
        total_price += product["price"] * item["quantity"]
        order_items.append({
            "product_id": str(product["_id"]),
            "name": product["name"],
            "quantity": item["quantity"],
            "price": product["price"]
        })

        # Mise à jour du stock
        products_collection.update_one({"_id": ObjectId(item["product_id"])}, {"$inc": {"stock": -item["quantity"]}})

    new_order = {
        "products": order_items,
        "total_price": total_price,
        "status": "pending"
    }
    order_id = orders_collection.insert_one(new_order).inserted_id
    return jsonify({"message": "Commande créée", "order_id": str(order_id)}), 201


@app.route('/orders/<user_id>', methods=['GET'])
def get_orders(user_id):
    """ Récupère les commandes d'un utilisateur """
    orders = list(orders_collection.find({"user_id": user_id}))
    for order in orders:
        order["_id"] = str(order["_id"])

    return jsonify(orders)


# ------------------ ROUTES PANIER ------------------

@app.route('/cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    """ Récupère le panier d'un utilisateur """
    cart = cart_collection.find_one({"user_id": user_id})
    if not cart:
        return jsonify({"cart": []})

    cart["_id"] = str(cart["_id"])
    return jsonify(cart)


@app.route('/cart/<user_id>', methods=['POST'])
def add_to_cart(user_id):
    """ Ajoute un produit au panier """
    data = request.json
    product = products_collection.find_one({"_id": ObjectId(data["product_id"])})

    if not product:
        return jsonify({"error": "Produit introuvable"}), 404

    cart_collection.update_one(
        {"user_id": user_id},
        {"$push": {"items": {"product_id": str(product["_id"]), "quantity": data["quantity"], "name": product["name"]}}},
        upsert=True
    )

    return jsonify({"message": "Produit ajouté au panier"})


@app.route('/cart/<user_id>/item/<product_id>', methods=['DELETE'])
def remove_from_cart(user_id, product_id):
    """ Supprime un produit du panier """
    cart_collection.update_one(
        {"user_id": user_id},
        {"$pull": {"items": {"product_id": product_id}}}
    )

    return jsonify({"message": "Produit retiré du panier"})


# ------------------ LANCEMENT DU SERVEUR ------------------

if __name__ == '__main__':
    app.run(debug=True)

