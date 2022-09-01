from collections import Counter
import numpy as np
from decimal import Decimal
import math
import random
import pandas as pd
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

L_2000 = 0
GE_2000_LE_4999 = 1
GE_5000_LE_9999 = 2
GE_10000_LE_14999 = 3
GE_15000_LE_19999 = 4
GE_20000_LE_24999 = 5
GE_25000_LE_29999 = 6
G_30000 = 7

def replace(count):
    if(count < 2000): return L_2000
    if(count >= 2000 and count <= 4999): return GE_2000_LE_4999
    if(count >= 5000 and count <= 9999): return GE_5000_LE_9999
    if(count >= 10000 and count <= 14999): return GE_10000_LE_14999
    if(count >= 15000 and count <= 19999): return GE_15000_LE_19999
    if(count >= 20000 and count <= 24999): return GE_20000_LE_24999
    if(count >= 25000 and count <= 29999): return GE_25000_LE_29999
    if(count >= 30000): return G_30000

def train_test_split(df, test_size=0.25):
    x_train = pd.DataFrame()
    x_test = pd.DataFrame()
    y_train = pd.DataFrame()
    y_test = pd.DataFrame()
    testRowCount = math.ceil(len(df) * test_size)
    rowsForTest = []
    i = 0
    while(i < testRowCount):
        randomNumber = random.randint(0, len(df) - 1)
        if(randomNumber not in rowsForTest):
            rowsForTest.append(randomNumber)
            i = i + 1
    for index, row in df.iterrows():
        df1 = df.loc[[index]]
        if(index in rowsForTest):
            x_test = pd.concat([x_test, df1.loc[:, df1.columns != 'price']])
            y_test = pd.concat([y_test, df1.loc[:, df1.columns == 'price']])
        else:
            x_train = pd.concat([x_train, df1.loc[:, df1.columns != 'price']])
            y_train = pd.concat([y_train, df1.loc[:, df1.columns == 'price']])

    return x_train, x_test, y_train, y_test


def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))

def manhattan_distance(x1, x2):
    return np.sum(np.abs(x1 - x2))


class KNN:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def predict(self, X):
        y_pred = [self._predict(x) for x in X]
        return np.array(y_pred)

    def _predict(self, x):
        # Compute distances between x and all examples in the training set
        distances = [manhattan_distance(x, x_train) for x_train in self.X_train]
        # Sort by distance and return indices of the first k neighbors
        k_idx = np.argsort(distances)[: self.k]
        # Extract the labels of the k nearest neighbor training samples
        k_neighbor_labels = [self.y_train[i][0] for i in k_idx]
        # return the most common class label
        most_common = Counter(k_neighbor_labels).most_common(1)
        return most_common[0][0]


def accuracy(y_true, y_pred):
        sum = np.sum(y_true == y_pred)
        accuracy = sum / len(y_true)
        return accuracy

conn = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'nedeljkovic1',
        database = 'polovniautomobili'
    )
curr = conn.cursor()

curr.execute("""select brand, city, color, price, subcategory, 
    productionYear, engineCapacity, enginePower, kilometers, 
    gearshift, seatsNumber, model, new_used, registrated, engineClass
    from polovni_automobili""")

df = pd.DataFrame(curr.fetchall(), columns=['brand', 'city', 'color', 'price', 'subcategory', 'productionYear',
    'engineCapacity', 'enginePower', 'kilometers', 'gearshift', 'seatsNumber', 'model', 'new_used', 'registrated', 'engineClass'])


all_brands = df.brand.unique()
brands_dict = dict(zip(all_brands, range(len(all_brands))))
df.brand.replace(brands_dict, inplace = True)

all_cities = df.city.unique()
cities_dict = dict(zip(all_cities, range(len(all_cities))))
df.city.replace(cities_dict, inplace = True)

all_colors = df.color.unique()
colors_dict = dict(zip(all_colors, range(len(all_colors))))
df.color.replace(colors_dict, inplace = True)

all_subcategories = df.subcategory.unique()
subcategories_dict = dict(zip(all_subcategories, range(len(all_subcategories))))
df.subcategory.replace(subcategories_dict, inplace = True)

all_models = df.model.unique()
models_dict = dict(zip(all_models, range(len(all_models))))
df.model.replace(models_dict, inplace = True)

all_engineClass = df.engineClass.unique()
engineClass_dict = dict(zip(all_engineClass, range(len(all_engineClass))))
df.engineClass.replace(engineClass_dict, inplace = True)

# plt.figure(figsize = (24,16))
# sns.heatmap(pd.concat([df.drop(['price'], axis=1),df['price']], axis=1).corr(), annot=True, cmap='coolwarm')
# plt.xticks(rotation=45, ha='right')
# plt.show()


df = df.drop(['brand', 'city', 'color', 'engineCapacity', 'seatsNumber', 'model', 
    'registrated', 'engineClass'], axis = 1)

df = df.dropna()

df = df.sort_values(by="price", ascending=True)

for feature in df.columns:
    if(feature != 'price'):
        mean_val = df[feature].mean()
        std_val = df[feature].std()
        df[feature] = (df[feature] - mean_val) / std_val
        #df[feature] = (df[feature] - df[feature].min()) / (df[feature].max() - df[feature].min())

x_train, x_test, y_train, y_test = train_test_split(df, test_size=0.001)


y_train['price'] = y_train['price'].apply(lambda x: replace(x))
y_test['price'] = y_test['price'].apply(lambda x: replace(x))


# x_train = (x_train - x_train.mean())/x_train.std()
# x_test = (x_test - x_test.mean())/x_test.std()

x_train.fillna(0, inplace=True)
x_test.fillna(0, inplace=True)


k = math.isqrt(df.shape[0])
if(k % 2 == 0):
    k = k + 1

change = input('Ukoliko zelite da promenite podrazumevanu vrednost parametra K, pritisnite 1: ')
if(change == '1'):
    while(True):
        k = input('Unesite vrednost parametra K(paran broj bice pretvoren u prvi veci neparni): ')
        try:
            k = int(k)
            if(k % 2 == 0):
                k = k + 1
            break
        except:
            print('GRESKA: Niste uneli broj!')
clf = KNN(k=k)
clf.fit(np.array(x_train), np.array(y_train))
predictions = clf.predict(np.array(x_test)) 
 

#print(y_test) 
print("KNN classification accuracy", accuracy(np.asarray(y_test).reshape(y_test.size), predictions)) 
#print(predictions)


# #====================== sklearn
# print("=============================")
# from sklearn.neighbors import KNeighborsClassifier
# classifier = KNeighborsClassifier(n_neighbors=3)
# classifier.fit(x_train, np.ravel(y_train,order='C'))
# y_pred = classifier.predict(x_test)
# print(y_pred)

# from sklearn import metrics
# print("Acc: ", metrics.accuracy_score(y_pred, y_test))


