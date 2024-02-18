import unittest
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
        self.access_token = self.user_service.login('base_user', 'base_user_pwd')

        # add second user
        self.user_service.register('second_user', 'second_user_pwd')
        self.second_access_token = self.user_service.login('second_user', 'second_user_pwd')
        
    def tearDown(self):
        self.ctx.pop()
        clear_database()

    def test_create_task(self):
        response = self.client.post('/api/v1/task', json={
            'name': 'Test Task'
        }, headers={'Authorization': 'Bearer ' + self.access_token})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['result']['name'], 'Test Task')
        return response.json['result']

    def test_get_tasks(self):
        task_id = self.test_create_task()['id']
        response = self.client.get('/api/v1/tasks', headers={'Authorization': 'Bearer ' + self.access_token})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json['result']) > 0)
        self.assertEqual(response.json['result'][0]['id'], task_id)

    def test_update_task(self):
        task_id = self.test_create_task()['id']
        response = self.client.put(f'/api/v1/task/{task_id}', json={
            'name': 'Updated Task',
            'status': 1
        }, headers={'Authorization': 'Bearer ' + self.access_token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Updated Task')
        self.assertEqual(response.json['status'], 1)
    
    def test_delete_task(self):
        task_id = self.test_create_task()['id']

        response = self.client.delete(f'/api/v1/task/{task_id}', headers={'Authorization': 'Bearer ' + self.access_token})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f'/api/v1/task/{task_id}', headers={'Authorization': 'Bearer ' + self.access_token})
        self.assertEqual(response.status_code, 404)

    def test_create_duplicate_task(self):
        task_name = self.test_create_task()['name']
        response = self.client.post('/api/v1/task', json={
            'name': task_name
        }, headers={'Authorization': 'Bearer ' + self.access_token})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], f'Task {task_name} already exists')

    def test_get_other_user_task(self):
        task_id = self.test_create_task()['id']
        response = self.client.get(f'/api/v1/task/{task_id}', headers={'Authorization': 'Bearer ' + self.second_access_token})
        self.assertEqual(response.status_code, 404)