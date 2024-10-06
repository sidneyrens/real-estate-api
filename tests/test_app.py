import unittest
from app import create_app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app, _ = create_app('testing')
        self.client = self.app.test_client()
        self.client.testing = True 

    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 404)

    def test_upload_route_exists(self):
        response = self.client.options('/upload')
        self.assertEqual(response.status_code, 200)