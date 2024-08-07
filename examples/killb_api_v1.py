import json
import os
from dotenv import load_dotenv
import requests as re
from mock.api_v1_mock_data import user_data, get_account_data

# Load environment variables from .env file
load_dotenv()


class KillBApiV1:
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
            response = self.make_request('POST', '/api/v1/accounts', json=get_account_data(user_id))
            print('Account created successfully:', response)
            return response.get('payload')
        except re.exceptions.HTTPError as err:
            print('Failed to create Account:', err)

    def quotation(self):
        """Create a new Quotation."""
        try:
            body = {
                "amount": "5000",
                "fromCurrency": "COP",
                "toCurrency": "USDT",
                "amountIsToCurrency": False
            }
            response = self.make_request('POST', '/api/v1/quotations', json=body)
            print('Quotation created successfully:', response)
            return response.get('payload')
        except re.exceptions.HTTPError as err:
            print('Failed to create Quotation:', err)

    def ramp(self, user_id: str, account_id: str, quotation_id: str):
        """Create a new RAMP."""
        body = {
            "quotationId": quotation_id,
            "userId": user_id,
            "accountId": account_id,
            "details": {
                "cashIn": {
                    "network": "PSE"
                }
            }
        }
        try:
            response = self.make_request('POST', '/api/v1/ramps/off', json=body)
            print('RAMP created successfully:', response)
            return response.get('payload')
        except re.exceptions.HTTPError as err:
            print('Failed to create RAMP:', err)


if __name__ == '__main__':
    """ 
    ****************************************** ENGLISH ******************************************
    This script demonstrates the process of creating and executing a RAMP using the API.

    Steps:

    1. Update the .env File:
       - Ensure that your .env file contains the necessary credentials from the SANDBOX or PRODUCTION environment.
       - This includes the EMAIL, PASSWORD, and API_KEY.

    2. Authentication:
       - Use the credentials from the .env file to authenticate with the API.
       - We highly recommend storing all sensitive data in the .env file to maintain security.

    3. Create a User:
       - In this example, we generate mock data to create a user.
       - This step simulates user creation to demonstrate the workflow.

    4. Create an Account:
       - Here, we create an account of type PSE.
       - You can create different types of accounts as specified in the API documentation.

    5. Create a Quotation:
       - Generate a quotation as part of the RAMP execution process.

    6. Execute a RAMP:
       - Finally, execute the RAMP using the previously created user, account, and quotation.

    ****************************************** SPANISH ******************************************
    Este script demuestra el proceso de crear y ejecutar un RAMP usando la API.

    Pasos:

    1. Actualizar el Archivo .env:
       - Asegúrate de que tu archivo .env contenga las credenciales necesarias del entorno SANDBOX o PRODUCCIÓN.
       - Esto incluye el EMAIL, PASSWORD y API_KEY.

    2. Autenticación:
       - Usa las credenciales del archivo .env para autenticarte con la API.
       - Recomendamos almacenar todos los datos sensibles en el archivo .env para mantener la seguridad.

    3. Crear un Usuario:
       - En este ejemplo, generamos datos ficticios para crear un usuario.
       - Este paso simula la creación de un usuario para demostrar el flujo de trabajo.

    4. Crear una Cuenta:
       - Aquí, creamos una cuenta de tipo PSE.
       - Puedes crear diferentes tipos de cuentas según lo especificado en la documentación de la API.

    5. Crear una Cotización:
       - Genera una cotización como parte del proceso de ejecución de RAMP.

    6. Ejecutar un RAMP:
       - Finalmente, ejecuta el RAMP usando el usuario, la cuenta y la cotización creados previamente.
    """

    apiV1 = KillBApiV1()

    apiV1.authenticate()

    user = apiV1.create_user()
    account = apiV1.create_account(user_id=user['id'])

    quotation = apiV1.quotation()
    ramp = apiV1.ramp(user_id=user['id'], account_id=account['id'], quotation_id=quotation['id'])
