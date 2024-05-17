import sqlite3

connection = sqlite3.connect('db.sqlite')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS auction(
        auction_id TEXT PRIMARY KEY,
        price INT,
        item_id TEXT,
        item_data TEXT
    )
''')

def store_item(auction_id, price, item_id, item_data):
    cursor.execute('''INSERT INTO auction (
        auction_id,
        price,
        item_id,
        item_data
    ) VALUES(?,?,?,?)
    ''', (auction_id, price, item_id, item_data))
    connection.commit()
