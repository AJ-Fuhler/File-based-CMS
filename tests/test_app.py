import unittest
from app import app

class CMSTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        self.assertEqual("text/html; charset=utf-8", response.content_type)
        self.assertIn("changes.txt", response.get_data(as_text=True))
        self.assertIn("history.txt", response.get_data(as_text=True))
        self.assertIn("about.md", response.get_data(as_text=True))

    
    def test_file_content(self):
        with self.client.get("/changes.txt") as response:
            self.assertEqual(200, response.status_code)
            self.assertEqual("text/plain; charset=utf-8", response.content_type)
            self.assertIn("many changes", response.get_data(as_text=True))
    
    def test_document_not_found(self):
        # Attempt to access a nonexistent file and verify a redirect happens
        with self.client.get("/notafile.ext") as response:
            self.assertEqual(302, response.status_code)

        # Verify redirect and message handling works
        with self.client.get(response.headers['Location']) as response:
            self.assertEqual(200, response.status_code)
            self.assertIn("notafile.ext does not exist",
                          response.get_data(as_text=True))
        
        # Assert that a page reload removes the message
        with self.client.get("/") as response:
            self.assertNotIn("notafile.ext does not exist",
                             response.get_data(as_text=True))
            
    def test_viewing_markdown_document(self):
        response = self.client.get('about.md')
        self.assertEqual(200, response.status_code)
        self.assertEqual("text/html; charset=utf-8", response.content_type)
        self.assertIn("<h1>Python is...</h1>",
                      response.get_data(as_text=True))
    
