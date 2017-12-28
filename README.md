Python RESTful API test
======================================

**Tasks**

The idea here is for us to see how you design a minimalistic API. This API will be 
used to perform CRUD operations on a model called User.

**Docker**

docker-compose build
docker-compose up

**Installation**

1. git clone https://github.com/eganichev/Python_RESTful_test.git
2. virtualenv -p python3.5 venv
3. source venv/bin/activate
4. cd Python_RESTful_test
5. pip install -r requirements.txt
6. if you want to edit configurations, change this in main.py 
    HOST = '0.0.0.0'
    DB_HOST = 'db'
7. python main.py

**Testing**

Run: python tests/test_main.py
