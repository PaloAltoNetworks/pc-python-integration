#Standard Library
import time
import logging

#Local
from ._session_types import CSPMSession, SaaSCWPSession

class SaaSSessionManager:
    def __init__(self, tenant_name: str, a_key: str, s_key: str, api_url: str, verify, logger):
        """
        Initializes a Prisma Cloud API Session Manager.

        Keyword Arguments:
        tenant_name -- Name of tenant associated with session
        a_key -- Tenant Access Key
        s_key -- Tenant Secret Key
        api_url -- API URL Tenant is hosted on 
        """
        self.logger = logger

        self.tenant = tenant_name
        self.a_key = a_key
        self.s_key = s_key
        self.api_url = api_url

        self.verify = verify

        self.cspm_session = {}
        self.saas_cwp_session = {}
        


#==============================================================================
    def create_cspm_session(self):
        session = CSPMSession(self.tenant, self.a_key, self.s_key, self.api_url, self.verify, logger=self.logger)
        self.cspm_session = session
        return session
    
    def create_cwp_session(self):
        if self.cspm_session:
            session = SaaSCWPSession(self.tenant, self.a_key, self.s_key, self.api_url, self.verify, logger=self.logger, cspm_session=self.cspm_session)
            self.saas_cwp_session = session
            return session
        else:
            self.create_cspm_session()
            session = SaaSCWPSession(self.tenant, self.a_key, self.s_key, self.api_url, self.verify, logger=self.logger, cspm_session=self.cspm_session)
            self.saas_cwp_session = session
            return session


#==============================================================================