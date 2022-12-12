import sqlite3


def db_create():
    connection = sqlite3.connect('dbphone.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS dbphone (id INTEGER PRIMARY KEY, surname TEXT, 
    name TEXT, phone_number TEXT, comments TEXT)''')
    connection.commit()
    connection.close()


# db_create()