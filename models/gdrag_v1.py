# linear regression on PET_GOLDEN_DRAGON pet exp and auction price

import json
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

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

petInfo = [json.loads(pet['item_data'])['petInfo'] for pet in pets]
features = np.reshape([min(pet['exp'], MAX_EXP) for pet in petInfo], (-1,1))
price = [pet['price'] for pet in pets]
features_train, features_test, price_train, price_test = train_test_split(features, price, test_size=0.3, random_state=42)

reg = LinearRegression()
reg.fit(features_train, price_train)
predictions = reg.predict(features)
score = reg.score(features_test, price_test)

print(f"Score: {score}")

plt.scatter(features, price)
plt.plot(features, predictions, color='red')
plt.xlabel("XP")
plt.ylabel("Coins")
plt.show()
