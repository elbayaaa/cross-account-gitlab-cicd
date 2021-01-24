import unittest
import requests
import os


class MyTest(unittest.TestCase):

    def runTest(self):
        url = "https://%s.execute-api.%s.amazonaws.com/Prod/hello/" % (os.getenv('API_DOMAIN'), os.getenv('REGION'))
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)
