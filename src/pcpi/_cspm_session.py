#Installed
import requests

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

#Local
from ._session_base import Session

import time

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CSPMSession(Session):
    def __init__(self, tenant_name: str, a_key: str, s_key: str, api_url: str, verify, logger):
        """
        Initializes a Prisma Cloud API session for a given tenant.

        Keyword arguments:
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

        self.token = ''

        self.auth_key = 'x-redlock-auth'
        self.auth_style = ''

        self.headers = {
            'content-type': 'application/json; charset=UTF-8',
            'x-redlock-auth': ''
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
        url = f'{self.api_url}/login'
        
        headers = {
            'content-type': 'application/json; charset=UTF-8'
            }

        payload = {
            "username": f"{self.a_key}",
            "password": f"{self.s_key}"
        }

        self.logger.debug('API - Generating CSPM session token.')
        res = object()
        try:
            start_time = time.time()
            self.logger.debug(url)
            res = requests.request("POST", url, headers=headers, json=payload, verify=self.verify)
            end_time = time.time()
            time_completed = round(end_time-start_time,3)

            self.token_time_stamp = time.time()
        except:
            self.logger.error('Failed to connect to API.')
            self.logger.warning('Make sure any offending VPNs are disabled.')

        return [res, time_completed]

    def _expired_login(self) -> None:
        self.logger.error('FAILED')
        self.logger.warning('Invalid Login Credentials. JWT not generated. Exiting...')
        exit()

    def _api_refresh(self) -> None:
            self.logger.debug('API - Refreshing SaaS session token.')

            res = object()
            try:
                start_time = time.time()
                self.logger.debug(self.api_url + '/auth_token/extend')
                res = requests.request("GET", self.api_url + '/auth_token/extend', headers=self.headers, verify=self.verify)
                end_time = time.time()
                time_completed = round(end_time-start_time,3)
                self.token_time_stamp = time.time()
            except:
                self.logger.error('Failed to connect to API.')
                self.logger.warning('Make sure any offending VPNs are disabled.')

            return [res, time_completed]
