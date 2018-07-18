import sqlite3
from flask import Flask, jsonify, request, abort
from argparse import ArgumentParser


DB = 'db.sqlite'

    
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return """<p>It works!</p>"""



@app.route('/api/admin/see_table/<string:table>', methods=['GET'])
def admin_get_table(table):
    parser = {
        'user':     parseUser,
        'task':     parseTask,
        'reminder':    parseReminder
    }
    data = fetchData(parser[table], f'SELECT * FROM {table}')
    return jsonify(data), 200

    
@app.route('/api/retrieve_task/<string:email>', methods=['GET'])
def retrieve_task(email):
    user_id = fetch_user_id(email)
    tasks = fetch_task(user_id)
    for task in tasks:
        task["reminder"] = fetch_reminder(task["id"])
    return jsonify(tasks), 200

@app.route('/api/create_task', methods=['POST'])
def create_task():
    if not request.json:
        abort(404)
        
    new_task = (
        request.json['user_id'],
        request.json['title'],
        request.json['content'],
        request.json['pinned'],
    )
    
    response = changeData("""
        INSERT INTO task (user_id,title,content,pinned)
        VALUES(?,?,?,?)
    """, new_task)

    return jsonify(response), 200    

@app.route('/api/delete_task', methods=['POST'])
def delete_task():
    if not request.json:
        abort(404)

    response = changeData("""
        DELETE FROM task WHERE id=?
    """, (request.json['task_id'],))
    
    return jsonify(response), 200

@app.route('/api/update_task', methods=['POST'])
def update_task():
    new_task = (
        request.json['title'],
        request.json['content'],
        request.json['pinned'],
        request.json['task_id'],
    )
    response = changeData("""
        UPDATE task 
        SET
            title   = ?,
            content = ?,
            pinned  = ?
        WHERE id = ?
    """, new_task)

    return jsonify(response), 200    


def fetch_reminder(task_id):
    return fetchData(parseReminder, 
    """
    SELECT * FROM reminder
    WHERE task_id = ?
    """, (task_id,))
    
def fetch_task(user_id):
    return fetchData(parseTask, 
    """
    SELECT * FROM task
    WHERE user_id = ?
    """, (user_id,))

def fetch_user_id(email):
    return fetchData(parseUser, 
    """
    SELECT * FROM user
    WHERE email = ?
    """, (email,))[0]["id"]



def parseUser(row):
    return {
        'id':         row[0],
        'email':     row[1],
    }
    
def parseTask(row):
    return {
        'id':         row[0],
        'user_id':     row[1],
        'title':     row[2],
        'content':     row[3],
        'pinned':     row[4],
    }

def parseReminder(row):
    return {
        'id':         row[0],
        'task_id':     row[1],
        'date':     row[2],
    }
    
def fetchData(parser, query, queryParam=None):
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    if queryParam:
        cursor.execute(query, queryParam)
    else:
        cursor.execute(query)
    rows = cursor.fetchall()
    db.close()
    result = []
    for row in rows:
        result.append(parser(row))
    return result

# Change means : INSERT, UPDATE or DELETE
def changeData(query, queryParam):
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    cursor.execute(query, queryParam)
    id = cursor.lastrowid
    db.commit()
    response = {
        'id': id,
        'affected': db.total_changes,
    }
    db.close()
    return response
    

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)