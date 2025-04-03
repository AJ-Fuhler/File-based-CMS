import unittest
from app import app

class AppTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        self.assertEqual("text/html; charset=utf-8", response.content_type)
        self.assertIn("changes.txt", response.get_data(as_text=True))
        self.assertIn("history.txt", response.get_data(as_text=True))
        self.assertIn("about.txt", response.get_data(as_text=True))

    
    def test_file_content(self):
        with self.client.get("/changes.txt") as response:
            self.assertEqual(200, response.status_code)
            self.assertEqual("text/plain; charset=utf-8", response.content_type)
            self.assertIn("many changes", response.get_data(as_text=True))
