import sqlite3
import time
from flask import Flask, jsonify, request, abort
from argparse import ArgumentParser


DB = 'db.sqlite'

    
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return """<p>It works!</p>"""

@app.route('/api/login', methods=['POST'])
def login():
    if not request.json:
        abort(404)
    
    user_id = fetch_user_id(request.json["email"], request.json["password"])

    session_id = int(round(time.time() * 1000))
    changeData("""
        INSERT INTO session (id, user_id)
        VALUES(?,?)
    """, (session_id, user_id))

    return jsonify({
        "matching_user_id": user_id,
        "session_id": session_id
    }), 200

@app.route('/api/logout', methods=['POST'])
def logout():
    if not request.json:
        abort(404)
    
    return jsonify(changeData("""
        DELETE FROM session
        WHERE id = ?
        """, (request.json["session_id"],))
    ) , 200


@app.route('/api/admin/see_table/<string:table>', methods=['GET'])
def admin_get_table(table):
    parser = {
        'user':     parseUser,
        'task':     parseTask,
        'reminder':    parseReminder
    }
    data = fetchData(parser[table], f'SELECT * FROM {table}')
    return jsonify(data), 200

    
@app.route('/api/task/<string:session_id>', methods=['GET'])
def retrieve_task(session_id):
    user_id = fetch_user_id_using_session(session_id)
    tasks = fetch_task(user_id)
    for task in tasks:
        task["reminder"] = fetch_reminder(task["id"])
    return jsonify(tasks), 200

@app.route('/api/task', methods=['POST'])
def create_task():
    if not request.json:
        abort(404)
        
    user_id = fetch_user_id_using_session(request.json["session_id"])

    new_task = (
        user_id,
        request.json['title'],
        request.json['content'],
        request.json['pinned']
    )
    
    response = changeData("""
        INSERT INTO task (user_id,title,content,pinned)
        VALUES(?,?,?,?)
    """, new_task)

    task_id = response["id"]

    # Insert reminders
    reminders = request.json["reminders"]
    for r in reminders:
        changeData("""
            INSERT INTO reminder(task_id, date)
            VALUES(?,?)
        """, (task_id, r["date"]))

    return jsonify(response), 200    

@app.route('/api/task', methods=['DELETE'])
def delete_task():
    if not request.json:
        abort(404)
    
    if not fetch_user_id_using_session(request.json["session_id"]):
        abort(404)

    response = changeData("""
        DELETE FROM task WHERE id=?
    """, (request.json['task_id'],))
    
    return jsonify(response), 200

@app.route('/api/task', methods=['PUT'])
def update_task():
    print(request.json["session_id"])
    if not fetch_user_id_using_session(request.json["session_id"]):
        abort(404)

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


    task_id = request.json['task_id']

    # Delete related reminders
    changeData("""
        DELETE FROM reminder WHERE task_id=?
    """, (task_id,))

    # Update reminders
    reminders = request.json["reminders"]

    for r in reminders:
        changeData("""
            INSERT INTO reminder(task_id, date)
            VALUES(?,?)
        """, (task_id, r["date"]))

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

def fetch_user_id_using_session(session_id):
    result = fetchData(parseSession,
    """
    SELECT * FROM session
    WHERE id = ?
    """, (session_id,))

    if len(result) > 0:
        return result[0]["user_id"]
    else:
        return None

def fetch_user_id(email, password):
    result = fetchData(parseUser, 
    """
    SELECT * FROM user
    WHERE email = ?
    AND password = ?
    """, (email,password))
    
    if len(result) > 0:
        return result[0]["id"]
    else:
        return None


def parseSession(row):
    return {
        'id':         row[0],
        'user_id':    row[1],
    }

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
