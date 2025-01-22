import unittest
import json
from app import app

class ChatbotTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_supplier_query(self):
        response = self.app.post('/chat', json={"user_input": "Tell me about the suppliers"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.json)

if __name__ == "__main__":
    unittest.main()
