import sqlite3
db = sqlite3.connect('db.sqlite')

db.execute('DROP TABLE IF EXISTS places')

db.execute('''
	CREATE TABLE user(
		id 		integer	PRIMARY KEY,
		email 	text 	UNIQUE NOT NULL
	)
''')

db.execute('''
	CREATE TABLE task(
		id 		integer PRIMARY KEY,
		user_id	integer,
		title 	text 	NOT NULL,
		content text 	NOT NULL,
		pinned 	integer NOT NULL,
		FOREIGN KEY(user_id) REFERENCES user(id)
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
    INSERT INTO user(name,city,date)
    VALUES('Forbidden City','Beijing','1274716800000')
''')


db.commit()
db.close()