import unittest
import time
from system.EnvLoader import EnvLoader
from tests.BaseTest import initialize_database, clear_database
from main import app
from model.UserDAO import UserDAO
from services.UserService import UserService

class TestUserCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        self.user_dao = UserDAO()
        self.user_service = UserService()
        initialize_database()
        # add base user
        self.user_service.register('base_user', 'base_user_pwd')
        
    def tearDown(self):
        self.ctx.pop()
        clear_database()

    def test_user_registration(self):
        response = self.client.post('/api/v1/user', json={
            'username': 'testcase',
            'password': 'testcase'
        })
        self.assertEqual(response.status_code, 201)

        user = self.user_dao.find_by_username('testcase')
        self.assertIsNotNone(user)

    def test_user_login(self):
        response = self.client.post('/api/v1/user/login', json={
            'username': 'base_user',
            'password': 'base_user_pwd'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json['access_token'])
    
    def test_user_info(self):
        access_token = self.user_service.login('base_user', 'base_user_pwd')
        response = self.client.get(
            '/api/v1/user', 
            headers={'Authorization': 'Bearer ' + access_token}
        )
        self.assertEqual(response.status_code, 200)

    def test_token_expired(self):
        EnvLoader.setenv('JWT_ACCESS_TOKEN_EXPIRES', str(1))
        access_token = self.user_service.login('base_user', 'base_user_pwd')
        time.sleep(2)
        response = self.client.get(
            '/api/v1/user', 
            headers={'Authorization': 'Bearer ' + access_token}
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['msg'], 'Token has expired')