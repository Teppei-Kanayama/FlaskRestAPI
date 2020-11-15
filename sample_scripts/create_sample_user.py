import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

insert_query = "INSERT INTO users VALUES (?, ?, ?)"

users = [
    (1, 'teppei', 'password1'),
    (2, 'kanayama', 'password2'),
    (3, 'test user', 'password3')
]
cursor.executemany(insert_query, users)

connection.commit()
connection.close()
