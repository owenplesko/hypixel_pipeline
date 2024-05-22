# regression model on PET_GOLDEN_DRAGON using exp, heldItem, skin to predict price

import json
import sqlite3
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge, Lasso, LassoLars
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

MAX_EXP = 210255385

def getPets():
    connection = sqlite3.connect('db.sqlite')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute('''
        SELECT * FROM auction WHERE item_id = 'PET_GOLDEN_DRAGON'
    ''')

    pets = cursor.fetchall()

    connection.close()
    
    return pets

pets = getPets()

price = [pet['price'] for pet in pets]

# create dataframe
df = pd.DataFrame([json.loads(pet['item_data'])['petInfo'] for pet in pets])
df = df[['exp', 'skin']]

# cap exp at pet max lvl
df['exp'] = df['exp'].clip(upper=210255385)

# create dummy values for heldItem and skin
df = pd.get_dummies(df)

X_train, X_test, y_train, y_test = train_test_split(df, price, test_size=0.3, random_state=13)

# linear model
reg = LinearRegression()
reg.fit(X_train, y_train)

print(f"Linear Score: {reg.score(X_test, y_test)}")
#print(pd.DataFrame({'Feature': df.columns, 'Coefficient': reg.coef_}))

## knn model
#reg = KNeighborsRegressor(n_neighbors=8)
#reg.fit(X_train, y_train)
#print(f"KNN Score: {reg.score(X_test, y_test)}")
#
## ridge model
#reg = Ridge(solver="auto")
#reg.fit(X_train, y_train)
#print(f"Ridge Score: {reg.score(X_test, y_test)}")
#
## lasso model
#reg = Lasso()
#reg.fit(X_train, y_train)
#print(f"Lasso Score: {reg.score(X_test, y_test)}")

# lassolars model
reg = LassoLars(alpha=0.1)
reg.fit(X_train, y_train)
print(f"LassoLars Score: {reg.score(X_test, y_test)}")
print(pd.DataFrame({'Feature': df.columns, 'Coefficient': reg.coef_}))

plt.scatter(df['exp'], price)
plt.scatter(df['exp'], reg.predict(df), color='red')
plt.xlabel("XP")
plt.ylabel("Coins")
plt.show()

