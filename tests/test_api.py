import base64
import unittest

from flask_testing import TestCase
from unittest.mock import ANY

from main import app, verify_password
from db.db_operations import get_region, get_user_by_username, get_all_ads_for_user, get_all_advertisements, create_user


class BaseTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app


class Test(BaseTestCase):
    def test_get_advertisement_by_region_id(self):
        credentials = base64.b64encode(b"user1:user1").decode('UTF-8')
        self.assert200(
            self.client.get('/api/v1/advertisement/byRegion/1', headers={'Authorization': f'Basic {credentials}'}))
        self.assert404(
            self.client.get('/api/v1/advertisement/byRegion/1000', headers={'Authorization': f'Basic {credentials}'}))
        self.assert403(
            self.client.get('/api/v1/advertisement/byRegion/2', headers={'Authorization': f'Basic {credentials}'}))

    def test_get_advertisement(self):
        self.assert200(self.client.get('/api/v1/advertisements'))

    def test_post_advertisement(self):
        credentials = base64.b64encode(b"user1:user1").decode('UTF-8')
        self.assert200(self.client.post('/api/v1/advertisement', json={
            "text": "text1",
            "status": "open",
            "region_id": 1,
            "category_id": 1,
            "user_id": 1}, headers={'Authorization': f'Basic {credentials}'}))
        self.assert403(self.client.post('/api/v1/advertisement', json={
            "text": "text1",
            "status": "open",
            "region_id": 1,
            "category_id": 1,
            "user_id": 2}, headers={'Authorization': f'Basic {credentials}'}))
        self.assert400(self.client.post('/api/v1/advertisement', json={}, headers={'Authorization': f'Basic {credentials}'}))

    def test_put_advertisement(self):
        credentials = base64.b64encode(b"user1:user1").decode('UTF-8')
        self.assert200(self.client.put('/api/v1/advertisement/1', json={"status": "close"}
                                       , headers={'Authorization': f'Basic {credentials}'}))
        self.assert403(self.client.put('/api/v1/advertisement/2', json={"status": "close"}
                                       , headers={'Authorization': f'Basic {credentials}'}))
        self.assert400(self.client.put('/api/v1/advertisement/1', json={}
                                       , headers={'Authorization': f'Basic {credentials}'}))
        self.assert404(self.client.put('/api/v1/advertisement/1000', json={"status": "close"}
                                       , headers={'Authorization': f'Basic {credentials}'}))

    def test_delete_advertisement(self):
        credentials = base64.b64encode(b"user1:user1").decode('UTF-8')
        self.assert404(self.client.delete('/api/v1/advertisement/2000', headers={'Authorization': f'Basic {credentials}'}))
        self.assert403(
            self.client.delete('/api/v1/advertisement/2', headers={'Authorization': f'Basic {credentials}'}))
        self.assert404(
            self.client.delete('/api/v1/advertisement/fdsfds', headers={'Authorization': f'Basic {credentials}'}))

    def test_post_user(self):
        self.assert200(self.client.post('/api/v1/auth/register', json={
            "username": "string3",
            "first_name": "string2",
            "last_name": "string2",
            "password": "string",
            "email": "string2@gmail.com",
            "region_id": 1
        }))
        self.assert400(self.client.post('/api/v1/auth/register', json={}))
        self.assert400(self.client.post('/api/v1/auth/register', json={
            "username": "string3",
            "first_name": "string2",
            "last_name": "string2",
            "password": "string",
            "email": "string2@gmail.com"
        }))
        self.assert400(self.client.post('/api/v1/auth/register', json={
            "username": "string3",
            "first_name": "string2",
            "last_name": "string2",
            "password": "string",
            "email": "string"
        }))
        self.assert400(self.client.post('/api/v1/auth/register', json={
            "username": "user1",
            "first_name": "string2",
            "last_name": "string2",
            "password": "string",
            "email": "string"
        }))

    def test_get_user(self):
        credentials = base64.b64encode(b"user1:user1").decode('UTF-8')
        self.assert200(self.client.get('/api/v1/user/user1', headers={'Authorization': f'Basic {credentials}'}))
        self.assert404(self.client.get('/api/v1/user/string3', headers={'Authorization': f'Basic {credentials}'}))
        self.assert404(self.client.get('/api/v1/user/string4', headers={'Authorization': f'Basic {credentials}'}))

    def test_index(self):
        self.assert200(self.client.get('/api/v1/hello-world/17'))

    def test_get_user_advertisements(self):
        credentials = base64.b64encode(b"user1:user1").decode('UTF-8')
        self.assert200(self.client.get('/api/v1/user/advertisements/1', headers={'Authorization': f'Basic {credentials}'}))
        self.assert404(
            self.client.get('/api/v1/user/advertisements/51321', headers={'Authorization': f'Basic {credentials}'}))
        self.assert403(
            self.client.get('/api/v1/user/advertisements/2', headers={'Authorization': f'Basic {credentials}'}))

    def test_verify_password(self):
        self.assertIs(verify_password('user1', 'user1'), True)
        self.assertIs(verify_password('user1', 'user2'), False)

    def test_get_region(self):
        resp = get_region(1)
        self.assertEqual(resp['name'], "Test Region")
        self.assertEqual(resp['id'], 1)

    def test_user_by_name(self):
        resp = get_user_by_username('user1')
        self.assertEqual(resp[0], 200)
        self.assertEqual(resp[1]['username'], 'user1')

    def test_get_all_ads_for_user(self):
        resp = get_all_ads_for_user(1)
        self.assertEqual(resp[0], 200)
        self.assertEqual(resp[1], ANY)

    def test_get_all_adds(self):
        resp = get_all_advertisements()
        self.assertEqual(resp[0], 200)
        self.assertEqual(resp[1], ANY)


if __name__ == '__main__':
    unittest.main()
