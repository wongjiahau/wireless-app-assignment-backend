import sqlite3
db = sqlite3.connect('db.sqlite')

db.execute('DROP TABLE IF EXISTS places')

db.execute('''
	CREATE TABLE user(
		id 		integer PRIMARY KEY AUTOINCREMENT,
		email 	text 	UNIQUE NOT NULL
	)
''')

db.execute('''
	CREATE TABLE task(
		id 		integer PRIMARY KEY AUTOINCREMENT,
		user_id	integer,
		title 	text 	NOT NULL,
		content text 	NOT NULL,
		pinned 	integer NOT NULL,
		FOREIGN KEY(user_id) REFERENCES user(id)
	)
''')

db.execute('''
	CREATE TABLE reminder(
		id 			integer PRIMARY KEY AUTOINCREMENT,
		task_id 	integer,
		date 		integer, 
		FOREIGN KEY(task_id) REFERENCES task(id)
	)
''')

cursor = db.cursor()

cursor.execute('''
    INSERT INTO task(email)
    VALUES('john@gmail.com')
''')

cursor.execute('''
    INSERT INTO task(email)
    VALUES('john@gmail.com')
''')


db.commit()
db.close()