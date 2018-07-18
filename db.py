import sqlite3
db = sqlite3.connect('db.sqlite')

db.execute('DROP TABLE IF EXISTS places')

db.execute('''
	CREATE TABLE task(
		id 		integer PRIMARY KEY,
		title 	text 	NOT NULL,
		content text 	NOT NULL,
		pinned 	integer NOT NULL
	)
''')

db.execute('''
	CREATE TABLE reminder(
		id 			integer PRIMARY KEY,
		task_id 	integer,
		date 		integer, 
		FOREIGN KEY(task_id) REFERENCES task(id)
	)
''')

cursor = db.cursor()

cursor.execute('''
    INSERT INTO places(name,city,date)
    VALUES('Forbidden City','Beijing','1274716800000')
''')


db.commit()
db.close()