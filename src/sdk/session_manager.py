import requests
from sdk.color_print import c_print

class Session:
    def __init__(self, tenant_name: str, a_key: str, s_key: str, api_url: str):
        """
        Initializes a Prisma Cloud API session for a given tenant.

        Keyword Arguments:
        tenant_name -- Name of tenant associated with session
        a_key -- Tenant Access Key
        s_key -- Tenant Secret Key
        api_url -- API URL Tenant is hosted on
        """
        self.tenant = tenant_name
        self.a_key = a_key
        self.s_key = s_key
        self.api_url = api_url
        self.token = self.__api_login()
        self.headers = {
            'content-type': 'application/json; charset=UTF-8',
            'x-redlock-auth': self.token
            }
        self.retries = 5
        self.retry_statuses = [429, 500, 502, 503, 504]
        c_print(f'Session created for tenant: {tenant_name}', color='green')
        print()

#==============================================================================

    def __api_login(self) -> None:
        '''
        Calls the Prisma Cloud API to generate a x-redlock-auth JWT.

        Returns:
        x-redlock-auth JWT.
        '''

        #Build request
        url = f'{self.api_url}/login'
        
        headers = {
            'content-type': 'application/json; charset=UTF-8'
            }

        payload = {
            "username": f"{self.a_key}",
            "password": f"{self.s_key}"
        }

        c_print('API - Generating session token.')
        response = requests.request("POST", url, headers=headers, json=payload)

        c_print(f'{url}', color='blue')

        #Results
        if response.status_code == 200:
            c_print('SUCCESS', color='green')
            print()
            token = response.json()['token']
            self.token = token
            self.headers = {
            'content-type': 'application/json; charset=UTF-8',
            'x-redlock-auth': token
            }
            return token
        elif response.status_code == 401:
            c_print('FAILED', end=' ', color='red')
            print('Invalid Login Credentials. JWT not generated.')
            print()
            self.token = 'BAD'
            return 'BAD'
        else:
            c_print('FAILED', end=' ', color='red')
            print('ERROR Logging In. JWT not generated.')
            print()
            self.token = 'BAD'

            c_print('RESPONSE:', color='yellow')
            print(response)
            c_print('RESPONSE URL:', color='yellow')
            print(response.url)
            c_print('RESPONSE TEXT:', color='yellow')
            print(response.text)
            
            return 'BAD'

#==============================================================================

    def __api_call_wrapper(self, method: str, url: str, json: dict=None, data: dict=None, params: dict=None, redlock_ignore: list=None, status_ignore: list=[]):
        """
        A wrapper around all API calls that handles token generation, retrying
        requests and API error console output logging.

        Keyword Arguments:
        method -- Request method/type. Ex: POST or GET
        url -- Full API request URL
        data -- Body of the request in a json compatible format
        params -- Queries for the API request

        Returns:
        Respose from API call.

        """
        c_print(f'{url}', color='blue')
        res = requests.request(method, url, headers=self.headers, json=json, data=data, params=params)
        
        if res.status_code == 200 or res.status_code in status_ignore:
            c_print('SUCCESS\n', color='green')
            return res
        
        c_print('--api_call_wrapper--', color='blue')
        if res.status_code == 401:
            c_print('Token expired. Generating new Token and retrying.', color='yellow')
            print()
            self.__api_login()
            c_print(f'{url}', color='blue')
            res = requests.request(method, url, headers=self.headers, json=json, data=data, params=params)

        retries = 0
        while res.status_code in self.retry_statuses and retries < self.retries:
            c_print(f'Retrying request. Code {res.status_code}.', color='yellow')
            c_print(f'{url}', color='blue')
            res = requests.request(method, url, headers=self.headers, json=json, data=data, params=params)
            retries += 1
        
            print() 
        
        if res.status_code == 200 or res.status_code in status_ignore:
            c_print('SUCCESS\n', color='green')
            return res

        #Some redlock errors need to be handled elsewhere and don't require this debugging output
        if 'x-redlock-status' in res.headers and redlock_ignore:
            for el in redlock_ignore:
                if el in res.headers['x-redlock-status']:
                    return res

        c_print('FAILED\nREQUEST DUMP:', color='red')
        c_print('REQUEST HEADERS:', color='yellow')
        print(self.headers)
        c_print('REQUEST JSON:', color='yellow')
        print(json)
        if data:
            c_print('REQUEST DATA:', color='yellow')
            print(data)
        c_print('REQUEST PARAMS:', color='yellow')
        print(params)
        c_print('RESPONSE:', color='yellow')
        print(res)
        c_print('RESPONSE URL:', color='yellow')
        print(res.url)
        c_print('RESPONSE HEADERS:', color='yellow')
        print(res.headers)
        c_print('RESPONSE REQUEST BODY:', color='yellow')
        print(res.request.body)
        c_print('RESPONSE STATUS:', color='yellow')
        if 'x-redlock-status' in res.headers:
            print(res.headers['x-redlock-status'])
        else:
            print()
        c_print('RESPONSE TEXT:', color='yellow')
        print(res.text)
        c_print('RESPONSE JSON:', color='yellow')
        if res.text != "":
            for json_data in res.json():
                print(json_data)
                print()
        else:
            print()
        print()

        return res

#==============================================================================

    def request(self, method: str, endpoint_url: str, json: dict=None, data: dict=None, params: dict=None, redlock_ignore: list=None, status_ignore: list=[]):
        '''
        Function for calling the PC API using this session manager. Accepts the
        same arguments as 'requests.request' minus the headers argument as 
        headers are supplied by the session manager.
        '''
        #Validate method
        method = method.upper()
        if method not in ['POST', 'PUT', 'GET', 'OPTIONS', 'DELETE', 'PATCH']:
            print('--request--')
            c_print('Invalid method.', color='red')
            print()
        
        #Build url
        if endpoint_url[0] != '/':
            endpoint_url = '/' + endpoint_url

        url = f'{self.api_url}{endpoint_url}'

        #Call wrapper
        return self.__api_call_wrapper(method, url, json=json, data=data, params=params, redlock_ignore=redlock_ignore, status_ignore=status_ignore)