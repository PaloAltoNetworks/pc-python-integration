import unittest
from unittest import mock
from unittest import TestCase
import os
import json

#Default Logger
import logging
logging.basicConfig()
py_logger = logging.getLogger("pcpi")
py_logger.setLevel(10)

#HELPER FUNCTIONS==============================================================
def load_environment():
    cfg = {}
    with open('local.json', "r") as file:
        cfg = json.load(file)

    #Parse cfg for tenant creds and set env
    for index,cred in enumerate(cfg):
        tenant = cred['name']
        uname = cred['identity']
        passwd = cred['secret']
        api_url = cred['url']
        verify = True
        try:
            verify = cred['verify']
            if verify.lower() == 'false':
                verify = False
            if verify.lower() == 'true':
                verify = True
        except:
            pass
            
        proxies = cred['proxies']
        https_proxy = ''
        http_proxy = ''
        if proxies:
            http_proxy = proxies.get('http','')
            https_proxy = proxies.get('https','')

        os.environ[f'PC_TENANT_NAME{index}'] = tenant
        os.environ[f'PC_TENANT_API{index}'] = api_url
        os.environ[f'PC_TENANT_A_KEY{index}'] = uname
        os.environ[f'PC_TENANT_S_KEY{index}'] = passwd
        os.environ[f'PC_TENANT_VERIFY{index}'] = str(verify)
        os.environ[f'PC_HTTP_PROXY{index}'] = http_proxy
        os.environ[f'PC_HTTPS_PROXY{index}'] = https_proxy

    
#UNIT TESTS====================================================================

class credentialFileTests(TestCase):
    def testLoadConfigBasic(self):
        load_environment()
        from src.pcpi import session_loader
        from src.pcpi import saas_session_manager
        name = os.environ['PC_TENANT_NAME0']
        api_url = os.environ['PC_TENANT_API0']
        a_key = os.environ['PC_TENANT_A_KEY0']
        s_key = os.environ['PC_TENANT_S_KEY0']
        verify = os.environ['PC_TENANT_VERIFY0']
        http = os.environ['PC_HTTP_PROXY0']
        https = os.environ['PC_HTTPS_PROXY0']
        proxies = {
            'http': http,
            'https': https
        }

        result = session_loader.load_config()
        self.assertEqual([result[0].tenant], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, proxies, py_logger).tenant])
        self.assertEqual([result[0].a_key], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, proxies, py_logger).a_key])
        self.assertEqual([result[0].s_key], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, proxies, py_logger).s_key])
        self.assertEqual([result[0].api_url], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, proxies, py_logger).api_url])


    def testLoadConfigEnv(self):
        load_environment()
        from src.pcpi import session_loader
        from src.pcpi import saas_session_manager
        name = os.environ['PC_TENANT_NAME0']
        api_url = os.environ['PC_TENANT_API0']
        a_key = os.environ['PC_TENANT_A_KEY0']
        s_key = os.environ['PC_TENANT_S_KEY0']
        verify = os.environ['PC_TENANT_VERIFY0']
        http = os.environ['PC_HTTP_PROXY0']
        https = os.environ['PC_HTTPS_PROXY0']
        proxies = {
            'http': http,
            'https': https
        }

        result = session_loader.load_config_env(prisma_name='PC_TENANT_NAME0', identifier_name='PC_TENANT_A_KEY0', secret_name='PC_TENANT_S_KEY0', api_url_name='PC_TENANT_API0', verify_name='PC_TENANT_VERIFY0', http_name='PC_HTTP_PROXY0', https_name='PC_HTTPS_PROXY0')
        self.assertEqual(result.tenant, saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, proxies, py_logger).tenant)
        self.assertEqual(result.a_key, saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, proxies, py_logger).a_key)
        self.assertEqual(result.s_key, saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, proxies, py_logger).s_key)
        self.assertEqual(result.api_url, saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, proxies, py_logger).api_url)

class apiRequestTest(TestCase):
    def testCSPMRecovery(self):
        from src.pcpi import session_loader
        manager = session_loader.load_config('local.json')[0]
        cspm_session = manager.create_cspm_session()
        res = cspm_session.request('GET', '/cloud')
        cspm_session.headers = {
            'content-type': 'application/json; charset=UTF-8',
            'x-redlock-auth': 'asd'
        }
        res1 = cspm_session.request('GET', '/cloud')

        self.assertEqual(res.json(), res1.json())

    def testCWPRecovery(self):
        from src.pcpi import session_loader
        manager = session_loader.load_config('local.json')[0]
        cwp_session = manager.create_cwp_session()
        res = cwp_session.request('GET', '/api/v1/users')
        cwp_session.headers = {
            'content-type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer dfsdfsd'
        }
        cwp_session.cspm_token = 'sdfsdf'
        res1 = cwp_session.request('GET', '/api/v1/users')

        self.assertEqual(res.json(), res1.json())

    def testCertBypass(self):
        from src.pcpi import session_loader
        manager = session_loader.load_config('local.json')[0]
        cspm_session = manager.create_cspm_session()
        res = cspm_session.request('GET', '/cloud', verify=False)

        self.assertEqual(res.status_code, 200)

    # def testCertOverwrite(self):
    #     from src.pcpi import session_loader
    #     manager = session_loader.load_from_file()
    #     cspm_session = manager.create_cspm_session()
    #     res = cspm_session.request('GET', '/compliance', verify='globalprotect_certifi.txt')

    #     self.assertEqual(res.status_code, 200)
        
if __name__ == '__main__':
    unittest.main()