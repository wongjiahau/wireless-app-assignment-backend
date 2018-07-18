import sqlite3
db = sqlite3.connect('db.sqlite')

db.execute('DROP TABLE IF EXISTS places')

db.execute('''CREATE TABLE places(
    id integer PRIMARY KEY,
    name text NOT NULL,
    city text NOT NULL,
    date integer NOT NULL
)''')

cursor = db.cursor()

cursor.execute('''
    INSERT INTO places(name,city,date)
    VALUES('Forbidden City','Beijing','1274716800000')
''')

cursor.execute('''
    INSERT INTO places(name,city,date)
    VALUES('Victoria Harbour','Hong Kong','1385481600000')
''')

cursor.execute('''
    INSERT INTO places(name,city,date)
    VALUES('Yarra Valley','Melbourne','1460908800000')
''')

cursor.execute('''
    INSERT INTO places(name,city,date)
    VALUES('Gamcheon Cultural Village','Busan','1495468800000')
''')

cursor.execute('''
    INSERT INTO places(name,city,date)
    VALUES('The Pinnacles','Perth','1508688000000')
''')

db.commit()
db.close()