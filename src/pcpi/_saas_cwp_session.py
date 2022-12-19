#Installed
import requests

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

#Local
from ._session_base import Session
from ._cspm_session import CSPMSession

#Python Library
import time

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SaaSCWPSession(Session):
    def __init__(self, tenant_name: str, a_key: str, s_key: str, api_url: str, verify, logger, cspm_session={}):
        """
        Initializes a Prisma Cloud API session for a given tenant.

        Keyword Arguments:
        tenant_name -- Name of tenant associated with session
        a_key -- Tenant Access Key
        s_key -- Tenant Secret Key
        api_url -- API URL Tenant is hosted on
        """

        super().__init__(logger)

        self.tenant = tenant_name
        self.a_key = a_key
        self.s_key = s_key
        self.api_url = api_url
        self.verify = verify

        self.token_time_stamp = 0

        self.logger = logger

        self.cspm_session = {}
        self.cspm_token = ''

        if not cspm_session:
            self.__get_cspm_session()
        else:
            self.cspm_session = cspm_session
            self.cspm_token = self.cspm_session.token

        self.api_url = self.__cwpp_metadata(self.cspm_session)

        self.auth_key = 'Authorization'
        self.auth_style = 'Bearer '
        
        self.token = ''

        self.headers = {
            'content-type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer '
        }

        self._api_login_wrapper()

#==============================================================================
    def __get_cspm_session(self):
        self.cspm_session = CSPMSession(self.tenant, self.a_key, self.s_key, self.api_url, self.verify, self.logger)
        self.cspm_token = self.cspm_session.token
    
    def __cspm_login(self):
        self.cspm_token = self.cspm_session._api_login_wrapper()

    def __cwpp_metadata(self, cspm_session):
        res = cspm_session.request('GET', 'meta_info')
        compute_url = res.json()['twistlockUrl']

        return compute_url

#==============================================================================
    def _api_login(self) -> object:
        '''
        Calls the Prisma Cloud API to generate a x-redlock-auth JWT.

        Returns:
        x-redlock-auth JWT.
        '''

        #Build request
        url = f'{self.api_url}/api/v1/authenticate'
        
        headers = {
            'content-type': 'application/json; charset=UTF-8'
            }

        payload = {
            "username": None,
            "password": None,
            "token": self.cspm_token
        }

        self.logger.debug('API - Generating SaaS CWPP session token.')

        res = object()
        try:
            start_time = time.time()
            self.logger.debug(url)
            res = requests.request("POST", url, headers=headers, json=payload, verify=self.verify)
            end_time = time.time()
            time_completed = round(end_time-start_time, 3)
            
            self.token_time_stamp = time.time()
        except:
            self.logger.error('Failed to connect to API.')
            self.logger.warning('Make sure any offending VPNs are disabled.')

        return [res, time_completed]

    def _expired_login(self) -> None:
        self.logger.warning('CSPM session expired. Generating new session.')
        self.__cspm_login()

    def _api_refresh(self) -> None:
        self.logger.debug('API - Refreshing SaaS session token.')

        res = object()
        try:
            res, time_completed = self.cspm_session._api_refresh()
            self.token_time_stamp = time.time()
        except:
            self.logger.error('Failed to connect to API.')
            self.logger.warning('Make sure any offending VPNs are disabled.')

        return [res, time_completed]