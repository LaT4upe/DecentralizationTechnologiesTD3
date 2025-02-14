import pandas as pd
import kagglehub
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

path = kagglehub.dataset_download("uciml/iris")

#print("Path to dataset files:", path)

db = pd.read_csv(path + '/Iris.csv')

X = db.drop(['Id', 'Species'], axis = 1)
y = db['Species']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)


clf = RandomForestClassifier()

clf.fit(X_train,y_train)

y_pred = clf.predict(X_test)


print(f'accuracy score : {metrics.accuracy_score(y_test, y_pred)}')
