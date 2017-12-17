Welcome to the Python RESTful API test
======================================


The objetive of this test if to help us evalute your skills with:

* Problem Solving
* Web Server API Design
* Request-time data manipulation
* Testing strategies
* Deployment

**Instructions**

* Fork the repo into a private repo.
* Create a virtualenv for this project and install requirements.txt file
* Modify the main module to complete the required API endpoints
* Let us know when you have finished.

**Tasks**

The idea here is for us to see how you design a minimalistic API. This API will be 
used to perform CRUD operations on a model called User.

You're free to design this model as you want, but, at a minimum should have:

* ID
* First name
* Last name
* Latitude
* Longitude

Check the main.py file, there you'll see you have to fullfill the following empty edges:

```python
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
def get_distances(user_id):
    """
    Each user has a lat/lon associated with them.  Determine the distance
    between each user pair, and provide the min/max/average/std as a json response.
    This should be GET only.
    You can use numpy or whatever suits you
    """
    return jsonify({})
```

This should be self-explanatory, we want you to fulfill the missing logic to generate expected 
responses.

It is important that you return correct response codes.


**Notes**

* The boilerplate code assumes you will use Flask, please stick to this
* Feel free to use any approach to deliver us the code..hint: A big bonus if you give us a Dockerfile we can just boot up and see application working
* Indicate what testing approach are you using...TDD, write code and test later, mocking, and tell us how to test your code
* Using MongoDB is required to store and retrieve data, you can use Flask-PyMongo or PyMongo, it is up to you.
* Try to adhere to Python etiquette (idiomatic and PEP-8 compliant code)
* For the distances endpoint, feel free to use any approach, although numpy will be highly beneficial here
* There is no need to write front-end code, but if you want to show off, build something that shows us your Angular-fu and 
makes our jaw drop, but only if you have extra time, this is not mandatory

**Questions**

* About the distances endpoint, please explain how would you scale this to hundreds and thousands of petitions per second, 
considering this is a CPU intensive endpoint. 
* How would you apporach this if latitude and longitude of user would be changing very frequently as well?  


**Deliverable**

Publish your work in a GitHub repository. Please use Python 3.x for your coding. Feel free to modify this readme to give any additional information a reviewer might need.
If you need more than 2 - 3 hours to do this, you might be overthinking, feel free to add improvement notes in your README file, show-off there :)


