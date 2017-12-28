import base64
from unittest.mock import patch

from flask import json
import main
import unittest
import random
from pymongo import MongoClient


class FlaskrTestCase(unittest.TestCase):

    headers = {'Authorization': 'Basic ' + base64.b64encode(b"username:password").decode("ascii")}

    @classmethod
    def setUpClass(cls):
        main.app.testing = True
        main.app = main.create_app(main.app, 'testrestdb', 'mongodb://localhost:27017/testprtdb', testable=True)
        cls.client = main.app.test_client()

    @classmethod
    def tearDownClass(self):
        client = MongoClient('localhost', 27017)
        client.drop_database('testprtdb')
        print("CLOSED")

    def test_create_user(self):
        response = self.client.post('/api/register', data=json.dumps(dict(username="username", password="password")),
                                    content_type='application/json')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEquals(data, {'username': 'username'})

    def test_login(self):
        response = self.client.post('/api/login', data=json.dumps(dict(username="username", password="password")),
                                    content_type='application/json')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEquals(data, {'username': 'username'})

    @patch('main.app.verify_session')
    def verify_session(self, mock_verify_session):
        mock_verify_session.return_value = True

    def test_create(self):
        print(self.headers)
        response = self.client.post('/prt/api/v1.0/users', data=json.dumps(dict(first_name="u1", last_name="uu1",
                                                                                lat=65.23, lon=10.2)),
                                    content_type='application/json', headers=self.headers)

        self.assertEquals(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEquals(data, {'result': 'OK'})

        response = self.client.post('/prt/api/v1.0/users', data=json.dumps(dict(first_name="u2", last_name="uu2",
                                                                                lat=15.23, lon=15.2)),
                                    content_type='application/json', headers=self.headers)
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEquals(data, {'result': 'OK'})

        response = self.client.post('/prt/api/v1.0/users', data=json.dumps(dict(first_name="u3", last_name="uu3",
                                                                                lat=35.23, lon=66.2)),
                                    content_type='application/json', headers=self.headers)
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEquals(data, {'result': 'OK'})

        response = self.client.post('/prt/api/v1.0/users', data=json.dumps(dict(first_name="u3")),
                                    content_type='application/json', headers=self.headers)
        self.assertEquals(response.status_code, 400)

    def test_get_all(self):
        all_users = self.client.get('/prt/api/v1.0/users', headers=self.headers)

        users_list = json.loads(all_users.data)
        self.assertEqual(len(users_list), 3)

    def test_update(self):
        all_users = self.client.get('/prt/api/v1.0/users', headers=self.headers)
        users_list = json.loads(all_users.data)

        u1 = random.choice(users_list)
        response = self.client.put('/prt/api/v1.0/users/' + u1["_id"],
                                   data=json.dumps(dict(first_name="new_u1", last_name="new_uu1",
                                                        lat=33.23, lon=55.2)),
                                   content_type='application/json', headers=self.headers)
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["first_name"], "new_u1")

        u2 = random.choice(users_list)
        response = self.client.put('/prt/api/v1.0/users/' + u2["_id"],
                                   data=json.dumps(dict(first_name="new_u2", last_name="new_uu2",
                                                        lat=35.23, lon=55.2)),
                                   content_type='application/json', headers=self.headers)
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["first_name"], "new_u2")

        u3 = random.choice(users_list)
        response = self.client.put('/prt/api/v1.0/users/' + u3["_id"], data=json.dumps(dict(first_name="u3")),
                                   content_type='application/json', headers=self.headers)
        self.assertEquals(response.status_code, 400)

    def test_distance(self):
        data = json.loads(self.client.get('/todo/api/v1.0/distances', headers=self.headers).data)
        self.assertEqual(len(data["distances"]), 3)
        self.assertEqual(data["stat"]["max"], 5574.1)
        self.assertEqual(data["stat"]["min"], 4932.14)
        self.assertLess(sum(i["dist"] for i in data["distances"]), 18000)

    def test_remove(self):
        all_users = self.client.get('/prt/api/v1.0/users', headers=self.headers)
        user = json.loads(all_users.data)[0]

        response = self.client.delete('/todo/api/v1.0/users/' + user["_id"], headers=self.headers)
        self.assertEqual(response.status_code, 200)

        all_users = self.client.get('/prt/api/v1.0/users', headers=self.headers)
        users_len = len(json.loads(all_users.data))
        self.assertEquals(users_len, 2)


if __name__ == '__main__':
    unittest.main()
