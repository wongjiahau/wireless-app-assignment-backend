import sqlite3
from flask import Flask, jsonify, request, abort
from argparse import ArgumentParser


DB = 'db.sqlite'


def get_row_as_dict(row):
    row_dict = {
        'id': row[0],
        'name': row[1],
        'city': row[2],
        'date': row[3],
    }

    return row_dict


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
	return """
	<p>Hello</p>
	"""


@app.route('/api/places', methods=['GET'])
def index():
    db = sqlite3.connect(DB)
    cursor = db.cursor()
    cursor.execute('SELECT * FROM places ORDER BY name')
    rows = cursor.fetchall()

    print(rows)

    db.close()

    rows_as_dict = []
    for row in rows:
        row_as_dict = get_row_as_dict(row)
        rows_as_dict.append(row_as_dict)

    return jsonify(rows_as_dict), 200


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