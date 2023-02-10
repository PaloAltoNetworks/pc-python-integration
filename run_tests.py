import unittest
from unittest import mock
from unittest import TestCase
import os
import yaml

#Default Logger
import logging
logging.basicConfig()
py_logger = logging.getLogger("pcpi")
py_logger.setLevel(10)

#HELPER FUNCTIONS==============================================================
def load_environment():
    cfg = {}
    with open('tenant_credentials.yml', "r") as file:
        cfg = yaml.load(file, Loader=yaml.BaseLoader)

    #Parse cfg for tenant creds and set env
    for index,tenant in enumerate(cfg):
        uname = cfg[tenant]['access_key']
        passwd = cfg[tenant]['secret_key']
        api_url = cfg[tenant]['api_url']
        verify = True
        try:
            verify = cfg[tenant]['verify']
            if verify.lower() == 'false':
                verify = False
            if verify.lower() == 'true':
                verify = True
        except:
            pass
        
        os.environ[f'PC_TENANT_NAME{index}'] = tenant
        os.environ[f'PC_TENANT_API{index}'] = api_url
        os.environ[f'PC_TENANT_A_KEY{index}'] = uname
        os.environ[f'PC_TENANT_S_KEY{index}'] = passwd
        os.environ[f'PC_TENANT_VERIFY{index}'] = str(verify)

def load_onprem_environment():
    cfg = {}
    with open('console_credentials.yml', "r") as file:
        cfg = yaml.load(file, Loader=yaml.BaseLoader)

    #Parse cfg for tenant names and create tokens for each tenant
    tenant_sessions = []
    for index,tenant in enumerate(cfg):
        uname = cfg[tenant]['uname']
        passwd = cfg[tenant]['passwd']
        api_url = cfg[tenant]['url']
        verify = True
        try:
            verify = cfg[tenant]['verify']
            if verify.lower() == 'false':
                verify = False
            if verify.lower() == 'true':
                verify = True
        except:
            pass
    
        os.environ[f'PC_CONSOLE_NAME{index}'] = tenant
        os.environ[f'PC_CONSOLE_API{index}'] = api_url
        os.environ[f'PC_CONSOLE_UNAME{index}'] = uname
        os.environ[f'PC_CONSOLE_PASSWD{index}'] = passwd
        os.environ[f'PC_CONSOLE_VERIFY{index}'] = str(verify)
    
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

        result = session_loader.load_config()
        self.assertEqual([result[0].tenant], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).tenant])
        self.assertEqual([result[0].a_key], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).a_key])
        self.assertEqual([result[0].s_key], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).s_key])
        self.assertEqual([result[0].api_url], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).api_url])

    def testLoadConfigFilePath(self):
        load_environment()
        from src.pcpi import session_loader
        from src.pcpi import saas_session_manager
        name = os.environ['PC_TENANT_NAME0']
        api_url = os.environ['PC_TENANT_API0']
        a_key = os.environ['PC_TENANT_A_KEY0']
        s_key = os.environ['PC_TENANT_S_KEY0']
        verify = os.environ['PC_TENANT_VERIFY0']

        result = session_loader.load_config(file_path='creds.json')
        self.assertEqual([result[0].tenant], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).tenant])
        self.assertEqual([result[0].a_key], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).a_key])
        self.assertEqual([result[0].s_key], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).s_key])
        self.assertEqual([result[0].api_url], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).api_url])

    def testLoadConfigEnv(self):
        load_environment()
        from src.pcpi import session_loader
        from src.pcpi import saas_session_manager
        name = os.environ['PC_TENANT_NAME0']
        api_url = os.environ['PC_TENANT_API0']
        a_key = os.environ['PC_TENANT_A_KEY0']
        s_key = os.environ['PC_TENANT_S_KEY0']
        verify = os.environ['PC_TENANT_VERIFY0']

        result = session_loader.load_config_env(prisma_name='PC_TENANT_NAME0', identifier_name='PC_TENANT_A_KEY0', secret_name='PC_TENANT_S_KEY0', api_url_name='PC_TENANT_API0', verify_name='PC_TENANT_VERIFY0')
        self.assertEqual(result.tenant, saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).tenant)
        self.assertEqual(result.a_key, saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).a_key)
        self.assertEqual(result.s_key, saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).s_key)
        self.assertEqual(result.api_url, saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).api_url)

    def testLoadMinFromFile(self):
        load_environment()
        from src.pcpi import session_loader
        from src.pcpi import saas_session_manager
        name = os.environ['PC_TENANT_NAME0']
        api_url = os.environ['PC_TENANT_API0']
        a_key = os.environ['PC_TENANT_A_KEY0']
        s_key = os.environ['PC_TENANT_S_KEY0']
        verify = os.environ['PC_TENANT_VERIFY0']

        name2 = os.environ['PC_TENANT_NAME1']
        api_url2 = os.environ['PC_TENANT_API1']
        a_key2 = os.environ['PC_TENANT_A_KEY1']
        s_key2 = os.environ['PC_TENANT_S_KEY1']
        verify2 = os.environ['PC_TENANT_VERIFY1']

        result = session_loader.load_min_from_file(2)
        self.assertEqual([result[0].tenant, result[1].tenant], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).tenant, saas_session_manager.SaaSSessionManager(name2, a_key2, s_key2, api_url2, verify2, py_logger).tenant])
        self.assertEqual([result[0].a_key, result[1].a_key], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).a_key, saas_session_manager.SaaSSessionManager(name2, a_key2, s_key2, api_url2, verify2, py_logger).a_key])
        self.assertEqual([result[0].s_key, result[1].s_key], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).s_key, saas_session_manager.SaaSSessionManager(name2, a_key2, s_key2, api_url2, verify2, py_logger).s_key])
        self.assertEqual([result[0].api_url, result[1].api_url], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).api_url, saas_session_manager.SaaSSessionManager(name2, a_key2, s_key2, api_url2, verify2, py_logger).api_url])

    def testLoadMultiFromFile(self):
        load_environment()
        from src.pcpi import session_loader
        from src.pcpi import saas_session_manager
        name = os.environ['PC_TENANT_NAME0']
        api_url = os.environ['PC_TENANT_API0']
        a_key = os.environ['PC_TENANT_A_KEY0']
        s_key = os.environ['PC_TENANT_S_KEY0']
        verify = os.environ['PC_TENANT_VERIFY0']

        name2 = os.environ['PC_TENANT_NAME1']
        api_url2 = os.environ['PC_TENANT_API1']
        a_key2 = os.environ['PC_TENANT_A_KEY1']
        s_key2 = os.environ['PC_TENANT_S_KEY1']
        verify2 = os.environ['PC_TENANT_VERIFY1']

        result = session_loader.load_multi_from_file(num_tenants=2)
        self.assertEqual([result[0].tenant, result[1].tenant], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).tenant, saas_session_manager.SaaSSessionManager(name2, a_key2, s_key2, api_url2, verify2, py_logger).tenant])
        self.assertEqual([result[0].a_key, result[1].a_key], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).a_key, saas_session_manager.SaaSSessionManager(name2, a_key2, s_key2, api_url2, verify2, py_logger).a_key])
        self.assertEqual([result[0].s_key, result[1].s_key], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).s_key, saas_session_manager.SaaSSessionManager(name2, a_key2, s_key2, api_url2, verify2, py_logger).s_key])
        self.assertEqual([result[0].api_url, result[1].api_url], [saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).api_url, saas_session_manager.SaaSSessionManager(name2, a_key2, s_key2, api_url2, verify2, py_logger).api_url])

    def testLoadFromFile(self):
        load_environment()
        from src.pcpi import session_loader
        from src.pcpi import saas_session_manager
        name = os.environ['PC_TENANT_NAME0']
        api_url = os.environ['PC_TENANT_API0']
        a_key = os.environ['PC_TENANT_A_KEY0']
        s_key = os.environ['PC_TENANT_S_KEY0']
        verify = os.environ['PC_TENANT_VERIFY0']

        result = session_loader.load_from_file()
        self.assertEqual(result.tenant, saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).tenant)
        self.assertEqual(result.a_key, saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).a_key)
        self.assertEqual(result.s_key, saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).s_key)
        self.assertEqual(result.api_url, saas_session_manager.SaaSSessionManager(name, a_key, s_key, api_url, verify, py_logger).api_url)

    def testOnpremLoadMinFromFile(self):
        load_onprem_environment()
        from src.pcpi import session_loader
        from src.pcpi import onprem_session_manager
        name = os.environ['PC_CONSOLE_NAME0']
        api_url = os.environ['PC_CONSOLE_API0']
        uname = os.environ['PC_CONSOLE_UNAME0']
        passwd = os.environ['PC_CONSOLE_PASSWD0']
        verify =  os.environ['PC_CONSOLE_VERIFY0']

        name2 = os.environ['PC_CONSOLE_NAME1']
        api_url2 = os.environ['PC_CONSOLE_API1']
        uname2 = os.environ['PC_CONSOLE_UNAME1']
        passwd2 = os.environ['PC_CONSOLE_PASSWD1']
        verify2 =  os.environ['PC_CONSOLE_VERIFY1']

        result = session_loader.onprem_load_min_from_file(2)

        self.assertEqual([result[0].tenant, result[1].tenant], [onprem_session_manager.CWPSessionManager(name, api_url, uname, passwd, verify, False, py_logger).tenant, onprem_session_manager.CWPSessionManager(name2, api_url2, uname2, passwd2, verify2, False, py_logger).tenant])
        self.assertEqual([result[0].uname, result[1].uname], [onprem_session_manager.CWPSessionManager(name, api_url, uname, passwd, verify, False, py_logger).uname, onprem_session_manager.CWPSessionManager(name2, api_url2, uname2, passwd2, verify2, False, py_logger).uname])
        self.assertEqual([result[0].passwd, result[1].passwd], [onprem_session_manager.CWPSessionManager(name, api_url, uname, passwd, verify, False, py_logger).passwd, onprem_session_manager.CWPSessionManager(name2, api_url2, uname2, passwd2, verify2, False, py_logger).passwd])
        self.assertEqual([result[0].api_url, result[1].api_url], [onprem_session_manager.CWPSessionManager(name, api_url, uname, passwd, verify, False, py_logger).api_url, onprem_session_manager.CWPSessionManager(name2, api_url2, uname2, passwd2, verify2, False, py_logger).api_url])

    def testOnpremLoadMultiFromFile(self):
        load_onprem_environment()
        from src.pcpi import session_loader
        from src.pcpi import onprem_session_manager
        name = os.environ['PC_CONSOLE_NAME0']
        api_url = os.environ['PC_CONSOLE_API0']
        uname = os.environ['PC_CONSOLE_UNAME0']
        passwd = os.environ['PC_CONSOLE_PASSWD0']
        verify =  os.environ['PC_CONSOLE_VERIFY0']

        name2 = os.environ['PC_CONSOLE_NAME1']
        api_url2 = os.environ['PC_CONSOLE_API1']
        uname2 = os.environ['PC_CONSOLE_UNAME1']
        passwd2 = os.environ['PC_CONSOLE_PASSWD1']
        verify2 =  os.environ['PC_CONSOLE_VERIFY1']

        result = session_loader.onprem_load_multi_from_file(num_tenants=2)

        self.assertEqual([result[0].tenant, result[1].tenant], [onprem_session_manager.CWPSessionManager(name, api_url, uname, passwd, verify, False, py_logger).tenant, onprem_session_manager.CWPSessionManager(name2, api_url2, uname2, passwd2, verify2, False, py_logger).tenant])
        self.assertEqual([result[0].uname, result[1].uname], [onprem_session_manager.CWPSessionManager(name, api_url, uname, passwd, verify, False, py_logger).uname, onprem_session_manager.CWPSessionManager(name2, api_url2, uname2, passwd2, verify2, False, py_logger).uname])
        self.assertEqual([result[0].passwd, result[1].passwd], [onprem_session_manager.CWPSessionManager(name, api_url, uname, passwd, verify, False, py_logger).passwd, onprem_session_manager.CWPSessionManager(name2, api_url2, uname2, passwd2, verify2, False, py_logger).passwd])
        self.assertEqual([result[0].api_url, result[1].api_url], [onprem_session_manager.CWPSessionManager(name, api_url, uname, passwd, verify, False, py_logger).api_url, onprem_session_manager.CWPSessionManager(name2, api_url2, uname2, passwd2, verify2, False, py_logger).api_url])

    def testOnpremLoadFromFile(self):
        load_onprem_environment()
        from src.pcpi import session_loader
        from src.pcpi import onprem_session_manager
        name = os.environ['PC_CONSOLE_NAME0']
        api_url = os.environ['PC_CONSOLE_API0']
        uname = os.environ['PC_CONSOLE_UNAME0']
        passwd = os.environ['PC_CONSOLE_PASSWD0']
        verify =  os.environ['PC_CONSOLE_VERIFY0']

        result = session_loader.onprem_load_from_file()

        self.assertEqual(result.tenant, onprem_session_manager.CWPSessionManager(name, api_url, uname, passwd, verify, False, py_logger).tenant)
        self.assertEqual(result.uname, onprem_session_manager.CWPSessionManager(name, api_url, uname, passwd, verify, False, py_logger).uname)
        self.assertEqual(result.passwd, onprem_session_manager.CWPSessionManager(name, api_url, uname, passwd, verify, False, py_logger).passwd)
        self.assertEqual(result.api_url, onprem_session_manager.CWPSessionManager(name, api_url, uname, passwd, verify, False, py_logger).api_url)

class apiRequestTest(TestCase):
    def testCSPMRecovery(self):
        from src.pcpi import session_loader
        manager = session_loader.load_from_file()
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
        manager = session_loader.load_from_file()
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
        manager = session_loader.load_from_file()
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