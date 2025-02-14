const API_URL = "http://127.0.0.1:5000";

async function getProducts() {
    try {
        let response = await fetch(`${API_URL}/products`);
        let products = await response.json();
        
        let productList = document.getElementById("product-list");
        productList.innerHTML = "";

        products.forEach(product => {
            let li = document.createElement("li");
            li.innerHTML = `${product.name} - ${product.price}€ 
                <button onclick="addToCart('${product._id}')">Ajouter au panier</button>`;
            productList.appendChild(li);
        });
    } catch (error) {
        console.error("Erreur de chargement des produits", error);
    }
}

// 🛒 Ajouter un produit au panier
async function addToCart(productId) {
    try {
        let response = await fetch(`${API_URL}/cart/user1`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ product_id: productId, quantity: 1 })
        });

        let result = await response.json();
        alert(result.message || "Produit ajouté au panier !");
    } catch (error) {
        console.error("Erreur d'ajout au panier", error);
    }
}

// Charger les produits quand la page s'affiche
if (document.getElementById("product-list")) {
    getProducts();
}
