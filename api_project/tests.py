import unittest
import warnings
from api import app

class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

    def test_getclients(self):
        response = self.app.get("/clients")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Reynard Surmon" in response.data.decode())

    def test_getclients_by_id(self):
        response = self.app.get("/clients/3")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Sybila Gleave" in response.data.decode())
    
    def test_getclient_address_by_client(self):
        response = self.app.get("/clients/4/clientaddress")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Tagopia" in response.data.decode())


if __name__ == "__main__":
    unittest.main()