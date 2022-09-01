from cmath import isnan
from decimal import Decimal
import math
import random
import pandas as pd
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np
import seaborn as sns

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

df.brand = df.brand.str.lower()
df.city = df.city.str.lower()
df.color = df.color.str.lower()
df.subcategory = df.subcategory.str.lower()
df.model = df.model.str.lower()
df.engineClass = df.engineClass.str.lower()

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
df_copy = df.copy()

for feature in df.columns:
    if(feature != 'price'):
        mean_val = df[feature].mean()
        std_val = df[feature].std()
        df[feature] = (df[feature] - mean_val) / std_val
        #df[feature] = (df[feature] - df[feature].min()) / (df[feature].max() - df[feature].min())


x_train, x_test, y_train, y_test = train_test_split(df, test_size=0.1)


ones_train = np.ones([len(x_train),1])
ones_test = np.ones([len(x_test),1])

# for feature in x_train.columns:
#     mean_val = x_train[feature].mean()
#     std_val = x_train[feature].std()
#     x_train[feature] = (x_train[feature] - mean_val) / std_val

# for feature in x_test.columns:
#     mean_val = x_test[feature].mean()
#     std_val = x_test[feature].std()
#     x_test[feature] = (x_test[feature] - mean_val) / std_val


x_train.fillna(0, inplace=True)
x_test.fillna(0, inplace=True)

x_train = np.concatenate((ones_train,x_train),axis=1)
x_test = np.concatenate((ones_test,x_test),axis=1)

theta = np.zeros([1,len(df.columns)])

#set hyper parameters
alpha = 0.01
iters = 1000

#computecost
def computeCost(X,y,theta):
    tobesummed = np.power(((X @ theta.T)-y),2)
    return np.sum(tobesummed)/(2 * len(X))

#gradient descent
def gradientDescent(X,y,theta,iters,alpha):
    cost = np.zeros(iters)
    for i in range(iters):
        theta = theta - (alpha/len(X)) * np.sum(X * (X @ theta.T - y), axis=0)
        cost[i] = computeCost(X, y, theta)
    
    return theta,cost


g,cost = gradientDescent(x_train,np.asarray(y_train),theta,iters,alpha)
pred = np.dot(x_test, g.T)
#print(cost)
print(y_test)
print(pred)

# #==================== scikit

# # importing module
# from sklearn.linear_model import LinearRegression
# # creating an object of LinearRegression class
# LR = LinearRegression()
# # fitting the training data


# LR.fit(x_train,y_train)

# y_prediction =  LR.predict(x_test)

# print(y_prediction)

# # Plot the convergence graph
# plt.plot(np.arange(iters), cost, '-b')
# plt.xlabel('Number of iterations')
# plt.ylabel('Cost J')
# plt.show()

def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

error = rmse(pred, y_test)['price']
print('Root mean squared error is:', error)

while(True):
    column = [[]]
    subcategory = input('Unesite karoseriju automobila:')
    subcategory = subcategory.lower()
    column[0].append(subcategory)
    productionYear = input('Unesite godinu proizvodnje:')
    try:
        productionYear = int(productionYear)
    except:
        print('GRESKA: Godina proizvodnje nije brojna vrednost!')
        continue
    column[0].append(productionYear)
    enginePower = input('Unesite snagu motora izrazenu u kW:')
    try:
        enginePower = int(enginePower)
    except:
        print('GRESKA: Snaga motora nije brojna vrednost!')
        continue
    column[0].append(enginePower)
    kilometers = input('Unesite kilometrazu automobila:')
    try:
        kilometers = int(kilometers)
    except:
        print('GRESKA: Kilometraza nije brojna vrednost!')
        continue
    column[0].append(kilometers)
    gearshift = input('Unesite 1 ukoliko automobil ima automatski menjac, a 0 ukoliko ima manuelni:')
    try:
        gearshift = int(gearshift)
        if(gearshift != 0 and gearshift != 1):
            print('GRESKA: Broj koji ste uneli nije 0 ili 1')
            continue
    except:
        print('GRESKA: Broj koji ste uneli nije 0 ili 1')
        continue
    column[0].append(gearshift)
    new_used = input('Unesite 1 ukoliko je u pitanju nov automobil, a 0 ukoliko je polovan:')
    try:
        new_used = int(new_used)
        if(new_used != 0 and new_used != 1):
            print('GRESKA: Broj koji ste uneli nije 0 ili 1')
            continue
    except:
        print('GRESKA: Broj koji ste uneli nije 0 ili 1')
        continue
    column[0].append(new_used)

    dataFrame = pd.DataFrame(column, columns=['subcategory', 'productionYear', 'enginePower', 'kilometers', 'gearshift', 'new_used'])
    dataFrame.subcategory = dataFrame.subcategory.str.lower()
    if(subcategory in subcategories_dict.keys()):
        dataFrame.subcategory.replace(subcategories_dict, inplace = True)
    else:
        dataFrame['subcategory'] = dataFrame['subcategory'].replace(subcategory, len(subcategories_dict) + 1)
    for feature in dataFrame.columns:
        mean_val = df_copy[feature].mean()
        std_val = df_copy[feature].std()
        dataFrame[feature] = (dataFrame[feature] - mean_val) / std_val
    ones = np.ones([len(dataFrame),1])
    features = np.concatenate((ones,dataFrame),axis=1)
    print('Predvidjena cena je:', np.dot(features, g.T)[0][0])
    cont = input('Unesite 1 ako zelite da unesete sledeci automobil:')
    if(cont != '1'):
        break