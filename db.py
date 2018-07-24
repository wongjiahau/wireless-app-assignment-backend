import sqlite3
db = sqlite3.connect('db.sqlite')

db.execute('DROP TABLE IF EXISTS places')

db.execute('''
	CREATE TABLE user(
		id 			integer PRIMARY KEY AUTOINCREMENT,
		email 		text 	UNIQUE NOT NULL,
		password 	text 	NOT NULL
	)
''')

db.execute('''
	CREATE TABLE session(
		id	 		integer PRIMARY KEY,
		user_id		integer,
		FOREIGN KEY(user_id) REFERENCES user(id)
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
		date 		integer, -- use epoch time in seconds
		FOREIGN KEY(task_id) REFERENCES task(id)
	)
''')

cursor = db.cursor()

# Insert one dummy user
cursor.execute('''
    INSERT INTO user(email,password)
    VALUES('john@gmail.com', '1234')
''')

# Insert two dummy tasks
cursor.execute('''
    INSERT INTO task(user_id, title, content, pinned)
    VALUES(1, 'Buy fruits', '2 apples', 0)
''')

cursor.execute('''
    INSERT INTO task(user_id, title, content, pinned)
    VALUES(1, 'Go shopping', 'at midvalley', 1)
''')

# Insert one dummy reminder
cursor.execute('''
    INSERT INTO reminder(task_id, date)
    VALUES(1, 1531881357799)
''')

# Insert one dummy session
cursor.execute('''
    INSERT INTO session(id, user_id)
    VALUES(1532420297001, 1)
''')


db.commit()
db.close()