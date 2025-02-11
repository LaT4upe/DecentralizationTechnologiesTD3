from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

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

# Prédiction sur les données test
y_pred = knn.predict(X_test)

# Évaluation
accuracy = accuracy_score(y_test, y_pred)
print(f"Précision du modèle KNN (k={k}): {accuracy:.2f}")

# Rapport de classification
print("\nRapport de classification:")
print(classification_report(y_test, y_pred))

# Matrice de confusion
print("\nMatrice de confusion:")
print(confusion_matrix(y_test, y_pred))
