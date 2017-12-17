#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
from flask_pymongo import PyMongo


app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()

app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/prtdb'
mongo_mgr = PyMongo(app)

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
    return jsonify({})


@app.route('/prt/api/v1.0/users/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    return jsonify({})


@app.route('/prt/api/v1.0/users', methods=['POST'])
@auth.login_required
def create_user():
    """
    Should add a new user to the users collection, with validation
    note: Always return the appropriate response for the action requested.
    """
    return jsonify({})


@app.route('/prt/api/v1.0/users/<int:user_id>', methods=['PUT'])
@auth.login_required
def update_user(user_id):
    """
    Update user specified with user ID and return updated user contents
    Note: Always return the appropriate response for the action requested.
    """
    return jsonify({})


@app.route('/todo/api/v1.0/users/<int:user_id>', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    """
    Delete user specified in user ID
    Note: Always return the appropriate response for the action requested.
    """
    return jsonify({})

@app.route('/todo/api/v1.0/distances', methods=['GET'])
@auth.login_required
def get_distances():
    """
    Each user has a lat/lon associated with them.  Determine the distance
    between each user pair, and provide the min/max/average/std as a json response.
    This should be GET only.
    You can use numpy or whatever suits you
    """
    return jsonify({})


if __name__ == '__main__':
    app.run(debug=True)
