#!flask/bin/python
import math
import itertools
import statistics
from flask import Flask, jsonify, abort, request, make_response, session
from flask_httpauth import HTTPBasicAuth
from flask_pymongo import PyMongo
from bson import ObjectId
from jsonschema import validate
from json_schema import json_user_schema, json_put_user_schema, JSONEncoder, json_client_schema
from passlib.hash import pbkdf2_sha256

auth = HTTPBasicAuth()
app = Flask(__name__, static_url_path="")
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

HOST = '0.0.0.0'
DB_HOST = 'db'


def create_app(app, db_name, db_uri, testable=False):
    if testable:
        app.config['MONGO2_DBNAME'] = db_name
        app.config['MONGO2_URI'] = db_uri
        app.mongo_mgr = PyMongo(app, config_prefix='MONGO2')
    else:
        app.config['MONGO_DBNAME'] = db_name
        app.config['MONGO_URI'] = db_uri
        app.mongo_mgr = PyMongo(app, config_prefix='MONGO')
    app.json_encoder = JSONEncoder
    return app


@app.route('/api/login', methods=['POST'])
def login():
    if not request.json:
        abort(400)
    else:
        username = request.json.get('username', '')
        password = request.json.get('password', '')
        if not (username or password):
            abort(400)  # missing arguments
        try:
            client = request.json
            validate(client, json_client_schema)
            login_user = app.mongo_mgr.db.credentials.find_one_or_404({'username': username})
            if login_user:
                if pbkdf2_sha256.verify(password, login_user['password']):
                    session['username'] = client['username']
                    return jsonify({'username': client['username']})

        except Exception as e:
            print(e)
            abort(400)


@app.route('/api/register', methods=['POST'])
def register():
    if not request.json:
        abort(400)
    else:
        username = request.json.get('username', '')
        password = request.json.get('password', '')

        if not (username or password):
            abort(400)
        elif app.mongo_mgr.db.credentials.find_one({'username': username}):
            abort(400)
        try:
            client = request.json
            client['password'] = pbkdf2_sha256.hash(password)
            validate(client, json_client_schema)
            app.mongo_mgr.db.credentials.insert(client)
            return jsonify({'username': client['username']})

        except Exception as e:
            print(e)
            abort(404)


@auth.verify_password
def verify_session(username, password):
    if username == 'username':
        return True
    else:
        return False


@auth.get_password
def get_password(username):
    if username == 'username':
        return 'password'
    return None


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/prt/api/v1.0/users', methods=['GET'])
@auth.login_required
def get_users():
    """
    Update this to return a json stream defining a listing of the users
    Note: Always return the appropriate response for the action requested.
    """
    users = [i for i in app.mongo_mgr.db.users.find({})]
    return jsonify(users)


@app.route('/prt/api/v1.0/users/<string:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    user = app.mongo_mgr.db.users.find_one_or_404({'_id': ObjectId(user_id)})
    return jsonify(user)


@app.route('/prt/api/v1.0/users', methods=['POST'])
@auth.login_required
def create_user():
    """
    Should add a new user to the users collection, with validation
    note: Always return the appropriate response for the action requested.
    """
    if not request.json:
        abort(400)
    else:
        try:
            user = request.json
            validate(user, json_user_schema)
            app.mongo_mgr.db.users.insert(user)
        except Exception as e:
            abort(400)
    return make_response(jsonify({'result': 'OK'}), 200)


@app.route('/prt/api/v1.0/users/<string:user_id>', methods=['PUT'])
@auth.login_required
def update_user(user_id):
    """
    Update user specified with user ID and return updated user contents
    Note: Always return the appropriate response for the action requested.
    """
    data = request.json
    if not data:
        abort(400)
    try:
        user = app.mongo_mgr.db.users.find_one_or_404({'_id': ObjectId(user_id)})
        validate(data, json_put_user_schema)
        app.mongo_mgr.db.users.update_one(user, {'$set': data})
    except Exception as e:
        abort(400)
    return make_response(jsonify(data), 200)


@app.route('/todo/api/v1.0/users/<string:user_id>', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    """
    Delete user specified in user ID
    Note: Always return the appropriate response for the action requested.
    """
    app.mongo_mgr.db.users.delete_one({'_id': ObjectId(user_id)})
    return make_response(jsonify({'result': 'OK'}), 200)


@app.route('/todo/api/v1.0/distances', methods=['GET'])
@auth.login_required
def get_distances():
    """
    Each user has a lat/lon associated with them.  Determine the distance
    between each user pair, and provide the min/max/average/std as a json response.
    This should be GET only.
    You can use numpy or whatever suits you
    """
    pairs = list(itertools.combinations(app.mongo_mgr.db.users.find({}), 2))
    distances = []
    for p1, p2 in pairs:
        distances.append({"id1": str(p1["_id"]),
                          "id2": str(p2["_id"]),
                          "dist": calculate_distance(p1['lat'], p1['lon'], p2['lat'], p2['lon'])})
    stat = {}
    print(distances)
    stat["min"] = min(i['dist'] for i in distances)
    stat["max"] = max(i['dist'] for i in distances)
    stat["avg"] = statistics.mean(i['dist'] for i in distances)
    stat["std"] = statistics.stdev(i['dist'] for i in distances)

    return jsonify({
        "distances": distances,
        "stat": stat
    })


def calculate_distance(lat1, long1, lat2, long2):
    radius = 6372.795   # Earth radius in km

    lat1 = lat1 * math.pi / 180.
    lat2 = lat2 * math.pi / 180.
    long1 = long1 * math.pi / 180.
    long2 = long2 * math.pi / 180.

    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y, x)
    return round(ad * radius, 2)


if __name__ == '__main__':
    app = create_app(app, 'restdb', 'mongodb://{}:27017/prtdb'.format(DB_HOST))
    app.run(debug=True, host=HOST)
