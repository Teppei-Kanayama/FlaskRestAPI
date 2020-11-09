import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()
cursor.execute("INSERT INTO items VALUES ('test_item', 99.99)")

connection.commit()
connection.close()
