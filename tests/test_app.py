import unittest
import shutil
import os
from app import app

class CMSTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.data_path = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(self.data_path, exist_ok=True)
    
    def tearDown(self):
        shutil.rmtree(self.data_path, ignore_errors=True)
    
    def create_document(self, name, content=""):
        with open(os.path.join(self.data_path, name), "w") as file:
            file.write(content)

    def test_index(self):
        self.create_document("about.md")
        self.create_document("changes.txt")


        response = self.client.get("/")

        self.assertEqual(200, response.status_code)
        self.assertEqual("text/html; charset=utf-8", response.content_type)
        self.assertIn("changes.txt", response.get_data(as_text=True))
        self.assertIn("about.md", response.get_data(as_text=True))

    
    def test_file_content(self):
        self.create_document("changes.txt", "There are many changes.")


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
        self.create_document("about.md", "<h1>Python is...</h1>")

        response = self.client.get('about.md')
        self.assertEqual(200, response.status_code)
        self.assertEqual("text/html; charset=utf-8", response.content_type)
        self.assertIn("<h1>Python is...</h1>",
                      response.get_data(as_text=True))
    
    def test_editing_document(self):
        self.create_document("changes.txt")

        response = self.client.get("/changes.txt/edit")
        self.assertEqual(200, response.status_code)
        self.assertIn("<textarea",
                      response.get_data(as_text=True))
        self.assertIn("<button type",
                      response.get_data(as_text=True))
    
    def test_updating_document(self):
        response = self.client.post("/changes.txt",
                                    data={'content': "new content"})
        self.assertEqual(302, response.status_code)

        follow_response = self.client.get(response.headers['Location'])
        self.assertIn("changes.txt has been updated.",
                      follow_response.get_data(as_text=True))
        
        with self.client.get("/changes.txt") as content_response:
            self.assertEqual(200, content_response.status_code)
            self.assertIn("new content",
                          content_response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()    
