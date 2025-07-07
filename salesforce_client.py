import os
import requests
from dotenv import load_dotenv

load_dotenv()

class SalesforceClient:
    def __init__(self):
        self.access_token = None
        self.instance_url = None
        self.authenticate()

    def authenticate(self):
        url = f"{os.getenv('SF_LOGIN_URL')}/services/oauth2/token"
        data = {
            'grant_type': 'password',
            'client_id': os.getenv('SF_CLIENT_ID'),
            'client_secret': os.getenv('SF_CLIENT_SECRET'),
            'username': os.getenv('SF_USERNAME'),
            'password': os.getenv('SF_PASSWORD') + os.getenv('SF_SECURITY_TOKEN')
        }

        res = requests.post(url, data=data)
        if res.status_code == 200:
            auth = res.json()
            self.access_token = auth['access_token']
            self.instance_url = auth['instance_url']
        else:
            raise Exception(f"Auth failed: {res.text}")

    def query(self, soql):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        url = f"{self.instance_url}/services/data/v58.0/query"
        res = requests.get(url, headers=headers, params={'q': soql})
        return res.json()
