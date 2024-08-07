from killb.client import Client
import json
import os
from dotenv import load_dotenv
import requests as re
from mock.api_v1_mock_data import user_data, get_account_data_wallet

# Load environment variables from .env file
load_dotenv()


class KillBApiV1WithV2:
    def __init__(self):
        self.base_url = os.getenv('KILLB_API_BASE_URL_V1')
        self.api_token = os.getenv('KILLB_API_TOKEN_V1')
        self.email = os.getenv('KILLB_CREDENTIALS_EMAIL')
        self.password = os.getenv('KILLB_CREDENTIALS_PASSWORD')
        self.access_token = None
        self.headers = {"x-api-key": self.api_token}

    def make_request(self, method, endpoint, data=None, files=None, json=None):
        """Make an API request."""
        try:
            url = f"{self.base_url}{endpoint}"
            response = re.request(method, url, headers=self.headers, data=data, files=files, json=json)
            response.raise_for_status()
            return response.json()
        except re.exceptions.HTTPError as err:
            print('Request failed:', err.response.json())

    def authenticate(self):
        """Authenticate to the API."""
        try:
            response = self.make_request('POST', '/api/v1/auth/login', data={
                "email": self.email,
                "password": self.password
            })
            self.access_token = response.get('accessToken')
            self.headers["Authorization"] = f"Bearer {self.access_token}"
            print('Authentication successful:', response)
        except re.exceptions.HTTPError as err:
            print('Authentication failed:', err)

    def create_user(self):
        """
            Create a new user using multipart form data.
            - This endpoint in V1 it is a MULTIPART, so the request should be this way
        """
        try:

            files = {'type': (None, 'PERSON', 'application/json'),
                     'data': (None, json.dumps(user_data), 'application/json')}
            response = self.make_request('POST', '/api/v1/users', files=files)
            print('User created successfully:', response)
            return response.get('payload')
        except re.exceptions.HTTPError as err:
            print('Failed to create user:', err)

    def create_account(self, user_id: str):
        """Create a new Account."""
        try:
            response = self.make_request('POST', '/api/v1/accounts', json=get_account_data_wallet(user_id))
            print('Account created successfully:', response)
            return response.get('payload')
        except re.exceptions.HTTPError as err:
            print('Failed to create Account:', err)


if __name__ == '__main__':
    client_api_v1 = KillBApiV1WithV2()

    client_v2 = Client(environment='SANDBOX', email=os.getenv('KILLB_CREDENTIALS_EMAIL_V2'),
                       password=os.getenv('KILLB_CREDENTIALS_PASSWORD_V2'), api_key=os.getenv('KILLB_API_TOKEN_V2'))

    client_api_v1.authenticate()
    user = client_api_v1.create_user()

    account = client_api_v1.create_account(user_id=user.get('id'))

    quotation = client_v2.Quotation.create(data={
        "fromCurrency": "COP",
        "toCurrency": "USDC",
        "amountIsToCurrency": False,
        "amount": 20000,
        "cashInMethod": "PSE",
        "cashOutMethod": "POLYGON"
    })

    print("QUOTATION V2 ----------> ", quotation)

    ramps = client_v2.Ramps.create(
        data={"quotationId": quotation.get('id'), "accountId": account.get('id'), "userId": user.get('id')})

    print("RAMPS V2 ----------> ", ramps)
