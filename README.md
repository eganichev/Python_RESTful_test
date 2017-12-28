Python RESTful API test
======================================

**Tasks**

The idea here is for us to see how you design a minimalistic API. This API will be 
used to perform CRUD operations on a model called User.

**Docker**

docker-compose build
docker-compose up

**Installation**
```
$ git clone https://github.com/eganichev/Python_RESTful_test.git
$ virtualenv -p python3.5 venv
$ source venv/bin/activate
$ cd Python_RESTful_test
$ pip install -r requirements.txt
```
if you want to edit configurations, change this in main.py 
```
HOST = '0.0.0.0'
DB_HOST = 'db'
```
```
python main.py
```

**Testing**

Run: 
```
python -m unittests tests/test_main.py
```
