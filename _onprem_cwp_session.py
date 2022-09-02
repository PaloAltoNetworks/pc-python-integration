#Standard Library
import enum

#Installed
import requests

#Local
from _session import Session

#Define enum type--------------------------------------------------------------
class SType(enum.Enum):
    basic = 1
    token = 2

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CWPSession(Session):
    def __init__(self, tenant_name: str, api_url: str, version: str, logger: object, uname='', passwd='', api_token=''):
        """
        Initializes a Prisma Cloud API session for a given tenant.

        Keyword Arguments:
        tenant_name -- Name of tenant associated with session
        api_url -- API URL Tenant is hosted on
        uname -- Username
        passwd -- Password
        token -- Dedicated API token
        """

        super().__init__(logger)

        self.tenant = tenant_name
        self.uname = uname
        self.passwd = passwd
        self.api_token = api_token
        self.version = version
        self.api_url = api_url

        self.logger = logger

        self.auth_key = 'Authorization'
        self.auth_style = 'Bearer '
        
        session_type = SType
        if uname != '' and passwd != '' and api_token == '':
            session_type = SType.basic
        elif api_token != '' and uname == '' and passwd == '':
            session_type = SType.token
        else:
            logger.error('Invalid credential configuration. Exiting...')
            exit()

        self.session_type = session_type

        self.headers = {
            'content-type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer '
        }

        self._api_login_wrapper()

#==============================================================================
    def _api_login(self) -> object:
        '''
        Calls the Prisma Cloud API to generate a x-redlock-auth JWT.

        Returns:
        x-redlock-auth JWT.
        '''

        #Build request
        url = f'{self.api_url}/api/{self.version}/authenticate'
        
        headers = {
            'content-type': 'application/json; charset=UTF-8'
            }

        payload = {}

        if self.session_type == SType.token:
            payload = {
                "username": None,
                "password": None,
                "token": self.token
            }
        else:
            payload = {
                "username": self.uname,
                "password": self.passwd,
                "token": None
            }

        self.logger.debug('API - Generating CWPP session token.')

        res = object()
        try:
            res = requests.request("POST", url, headers=headers, json=payload)
        except:
            self.logger.error('Failed to connect to API.')
            self.logger.warning('Make sure any offending VPNs are disabled.')
            self.logger.info('Exiting...')
            quit()

        return res

    def _expired_login(self) -> None:
        self.logger.warning('CSPM session expired. Generating new session.')
        self.__cspm_login()