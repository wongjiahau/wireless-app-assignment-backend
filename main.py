import sqlite3
from flask import Flask, jsonify, request, abort
from argparse import ArgumentParser


DB = 'db.sqlite'


def parseUser(row):
    return {
        'id': 		row[0],
        'email': 	row[1],
    }
	
def parseTask(row):
    return {
        'id': 		row[0],
        'user_id': 	row[1],
		'title': 	row[2],
		'content': 	row[3],
		'pinned': 	row[4],
    }

def parseReminder(row):
    return {
        'id': 		row[0],
        'task_id': 	row[1],
		'date': 	row[2],
    }
	
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
	return """<p>It works!</p>"""


@app.route('/api/users', methods=['GET'])
def users():
	return fetchData('SELECT * from USER', parseUser)

def fetchData(query, parser):
	db = sqlite3.connect(DB)
	cursor = db.cursor()
	cursor.execute(query)
	rows = cursor.fetchall()
	db.close()
	result = []
	for row in rows:
		result.append(parser(row))
	return jsonify(result), 200

@app.route('/api/places/<int:place>', methods=['GET'])
def show(place):
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    cursor.execute('SELECT * FROM places WHERE id=?', (str(place),))
    row = cursor.fetchone()
    db.close()

    if row:
        row_as_dict = get_row_as_dict(row)
        return jsonify(row_as_dict), 200
    else:
        return jsonify(None), 200


@app.route('/api/places', methods=['POST'])
def store():
    if not request.json:
        abort(404)

    new_place = (
        request.json['name'],
        request.json['city'],
        request.json['date'],
    )

    db = sqlite3.connect(DB)
    cursor = db.cursor()

    cursor.execute('''
        INSERT INTO places(name,city,date)
        VALUES(?,?,?)
    ''', new_place)

    place_id = cursor.lastrowid

    db.commit()

    response = {
        'id': place_id,
        'affected': db.total_changes,
    }

    db.close()

    return jsonify(response), 201


@app.route('/api/places/<int:place>', methods=['PUT'])
def update(place):
    if not request.json:
        abort(400)

    if 'id' not in request.json:
        abort(400)

    if int(request.json['id']) != place:
        abort(400)

    update_place = (
        request.json['name'],
        request.json['city'],
        request.json['date'],
        str(place),
    )

    db = sqlite3.connect(DB)
    cursor = db.cursor()

    cursor.execute('''
        UPDATE places SET
            name=?,city=?,date=?
        WHERE id=?
    ''', update_place)

    db.commit()

    response = {
        'id': place,
        'affected': db.total_changes,
    }

    db.close()

    return jsonify(response), 201


@app.route('/api/places/<int:place>', methods=['DELETE'])
def delete(place):
    if not request.json:
        abort(400)

    if 'id' not in request.json:
        abort(400)

    if int(request.json['id']) != place:
        abort(400)

    db = sqlite3.connect(DB)
    cursor = db.cursor()

    cursor.execute('DELETE FROM places WHERE id=?', (str(place),))

    db.commit()

    response = {
        'id': place,
        'affected': db.total_changes,
    }

    db.close()

    return jsonify(response), 201


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)