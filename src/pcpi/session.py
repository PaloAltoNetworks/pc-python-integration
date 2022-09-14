#Standard Library
import os
import re

#Installed
import yaml
import requests
import logging

#Default Logger
py_logger = logging.getLogger()
py_logger.setLevel(10)

#Local
from .saas_session_manager import SaaSSessionManager
from .onprem_session_manager import CWPSessionManager

def __c_print(*args, **kwargs):
    '''
    Uses ascii codes to enable colored print statements. Works on Mac, Linux and Windows terminals
    '''

    #Magic that makes colors work on windows terminals
    os.system('')
    
    #Define Colors for more readable output
    c_gray = '\033[90m'
    c_red = '\033[91m'
    c_green = '\033[92m'
    c_yellow = '\033[93m'
    c_blue = '\033[94m'
    c_end = '\033[0m'

    color = c_end
    if 'color' in kwargs:
        c = kwargs['color'].lower()
        if c == 'gray' or c == 'grey':
            color = c_gray
        elif c ==  'red':
            color = c_red
        elif c == 'green':
            color = c_green
        elif c == 'yellow':
            color = c_yellow
        elif c == 'blue':
            color = c_blue
        else:
            color = c_end

    _end = '\n'
    if 'end' in kwargs:
        _end = kwargs['end']

    print(f'{color}', end='')
    for val in args:
        print(val, end='')
    print(f'{c_end}', end=_end)

#==============================================================================

def __validate_cwp_credentials(name, _url, uname, passwd) -> bool:
    '''
    This function creates a session with the supplied credentials to test 
    if the user successfully entered valid credentials.
    '''

    headers = {
    'content-type': 'application/json; charset=UTF-8'
    }

    payload = {
        "username": uname,
        "password": passwd,
    }

    url = f'{_url}/api/v1/authenticate'

    try:
        __c_print('API - Validating credentials')
        res = requests.request("POST", url, headers=headers, json=payload)
        print(res.status_code)

        if res.status_code == 200:
            __c_print('SUCCESS', color='green')
            print()
            return True
        else:
            return False
    except:
        __c_print('ERROR', end=' ', color='red')
        print('Could not connect to Prisma Cloud API.')
        print()
        print('Steps to troubleshoot:')
        __c_print('1) Please disconnect from any incompatible VPN', color='blue')
        print()
        __c_print('2) Please ensure you have entered a valid Prisma Cloud URL.', color='blue')
        print()
        quit()
        return False

def __validate_credentials(a_key, s_key, url) -> bool:
    '''
    This function creates a session with the supplied credentials to test 
    if the user successfully entered valid credentials.
    '''

    headers = {
    'content-type': 'application/json; charset=UTF-8'
    }

    payload = {
        "username": f"{a_key}",
        "password": f"{s_key}"
    }

    try:
        __c_print('API - Validating credentials')
        response = requests.request("POST", f'{url}/login', headers=headers, json=payload)

        if response.status_code == 200:
            __c_print('SUCCESS', color='green')
            print()
            return True
        else:
            return False
    except:
        __c_print('ERROR', end=' ', color='red')
        print('Could not connect to Prisma Cloud API.')
        print()
        print('Steps to troubleshoot:')
        __c_print('1) Please disconnect from any incompatible VPN', color='blue')
        print()
        __c_print('2) Please ensure you have entered a valid Prisma Cloud URL.', color='blue')
        print('EX: https://app.prismacloud.io or https://app2.eu.prismacloud.io')
        print()
        return False

#==============================================================================

def __validate_url(url):
    if len(url) >= 3:
        if 'https://' not in url:
            if url[:3] == 'app' or url[:3] == 'api':
                url = 'https://' + url
            
    
    url = url.replace('app', 'api')

    url = re.sub(r'prismacloud\.io\S*', 'prismacloud.io', url)

    return url

#==============================================================================

def __get_cwp_tenant_credentials():

    __c_print('Enter tenant name or any preferred identifier (optional):', color='blue')
    name = input()

    __c_print('Enter console base url with port number:', color='blue')
    url = input()
    print()

    __c_print('Enter console username:', color='blue')
    uname = input()
    print()

    __c_print('Enter console password:', color='blue')
    passwd = input()
    print()
    

    return name, url, uname, passwd

def __get_tenant_credentials():

    __c_print('Enter tenant name or any preferred identifier:', color='blue')
    name = input()

    __c_print('Enter tenant url. (ex: https://app.ca.prismacloud.io):', color='blue')
    url = input()
    print()
    new_url = __validate_url(url)
    if new_url != url:
        __c_print('Adjusted URL:',color='yellow')
        print(new_url)
        print()

    __c_print('Enter tenant access key:', color='blue')
    a_key = input()
    print()

    __c_print('Enter tenant secret key:', color='blue')
    s_key = input()
    print()
    

    return name, a_key, s_key, new_url

#==============================================================================

def __build_cwp_session_dict(name, url, uname, passwd):
    session_dict = {
        name: {
            'url': url,
            'uname': uname,
            'passwd': passwd
            }
    }
    return session_dict

def __build_session_dict(name, a_key, s_key, url):
    session_dict = {
        name: {
            'access_key': a_key,
            'secret_key': s_key,
            'api_url': url
            }
    }
    return session_dict

#==============================================================================

def __get_cwp_credentials_from_user(num_tenants):
    #Gets the source tenant credentials and ensures that are valid
    credentials = []

    if num_tenants != -1:
        for i in range(num_tenants):
            valid = False
            while not valid:
                __c_print('Enter credentials for the console', color='blue')
                print()
                name, url, uname, passwd = __get_cwp_tenant_credentials()
                
                valid = __validate_cwp_credentials(name, url, uname, passwd)
                if valid == False:
                    __c_print('FAILED', end=' ', color='red')
                    print('Invalid credentials. Please re-enter your credentials')
                    print()
                else:
                    credentials.append(__build_cwp_session_dict(name, url, uname, passwd))

        return credentials
    else:
        while True:
            valid = False
            while not valid:
                __c_print('Enter credentials for the console', color='blue')
                print()
                name, url, uname, passwd = __get_cwp_tenant_credentials()
                
                valid = __validate_cwp_credentials(name, url, uname, passwd)
                if valid == False:
                    __c_print('FAILED', end=' ', color='red')
                    print('Invalid credentials. Please re-enter your credentials')
                    print()
                else:
                    credentials.append(__build_cwp_session_dict(name, url, uname, passwd))
            
            __c_print('Would you like to add an other tenant? Y/N')
            choice = input().lower()

            if choice != 'yes' and choice != 'y':
                break

        return credentials


def __get_credentials_from_user(num_tenants):
    #Gets the source tenant credentials and ensures that are valid
    credentials = []

    if num_tenants != -1:
        for i in range(num_tenants):
            valid = False
            while not valid:
                __c_print('Enter credentials for the tenant', color='blue')
                print()
                src_name, src_a_key, src_s_key, src_url = __get_tenant_credentials()
                
                valid = __validate_credentials(src_a_key, src_s_key, src_url)
                if valid == False:
                    __c_print('FAILED', end=' ', color='red')
                    print('Invalid credentials. Please re-enter your credentials')
                    print()
                else:
                    credentials.append(__build_session_dict(src_name, src_a_key, src_s_key, src_url))

        return credentials
    else:
        while True:
            valid = False
            while not valid:
                __c_print('Enter credentials for the tenant', color='blue')
                print()
                src_name, src_a_key, src_s_key, src_url = __get_tenant_credentials()
                
                valid = __validate_credentials(src_a_key, src_s_key, src_url)
                if valid == False:
                    __c_print('FAILED', end=' ', color='red')
                    print('Invalid credentials. Please re-enter your credentials')
                    print()
                else:
                    credentials.append(__build_session_dict(src_name, src_a_key, src_s_key, src_url))
            
            __c_print('Would you like to add an other tenant? Y/N')
            choice = input().lower()

            if choice != 'yes' and choice != 'y':
                break

        return credentials

def __load_uuid_yaml(file_name, logger=py_logger):
    with open(file_name, "r") as file:
        cfg = yaml.load(file, Loader=yaml.BaseLoader)

    credentials = cfg['credentials']
    entity_type = cfg['type']
    uuid = cfg['uuid']
    cmp_type = cfg['cmp_type']

    tenant_sessions = []
    for tenant in credentials:
        tenant_name = ''
        tenant_keys = tenant.keys()
        for name in tenant_keys:
            tenant_name = name     

        a_key = tenant[tenant_name]['access_key']
        s_key = tenant[tenant_name]['secret_key']
        api_url = tenant[tenant_name]['api_url']

        tenant_sessions.append(SaaSSessionManager(tenant_name, a_key, s_key, api_url, logger))

    return tenant_sessions, entity_type, uuid, cmp_type


#==============================================================================
def onprem_load_multi_from_file(file_path='console_credentials.yml', logger=py_logger, num_tenants=-1) -> list:
    '''
    Reads console_credentials.yml or specified file path to load
    self hosted CWP console credentials to create a session.
    Returns a CWP session object.
    '''
    #Open and load config file
    if not os.path.exists(file_path):
        #Create credentials yml file
        __c_print('No credentials file found. Generating...', color='yellow')
        print()
        tenants = __get_cwp_credentials_from_user(num_tenants)
        with open(file_path, 'w') as yml_file: 
            for tenant in tenants:
                yaml.dump(tenant, yml_file, default_flow_style=False)

    cfg = {}
    with open(file_path, "r") as file:
        cfg = yaml.load(file, Loader=yaml.BaseLoader)

    #Parse cfg for tenant names and create tokens for each tenant
    tenant_sessions = []
    for tenant in cfg:
        uname = cfg[tenant]['uname']
        passwd = cfg[tenant]['passwd']
        api_url = cfg[tenant]['api_url']

        tenant_sessions.append(CWPSessionManager(tenant, api_url, uname=uname, passwd=passwd, logger=logger))


    return tenant_sessions

def onprem_load_from_file(file_path='console_credentials.yml', logger=py_logger) -> list:
    '''
    Reads console_credentials.yml or specified file path to load
    self hosted CWP console credentials to create a session.
    Returns a CWP session object.
    '''
    #Open and load config file
    if not os.path.exists(file_path):
        #Create credentials yml file
        __c_print('No credentials file found. Generating...', color='yellow')
        print()
        tenants = __get_cwp_credentials_from_user(1)
        with open(file_path, 'w') as yml_file: 
            for tenant in tenants:
                yaml.dump(tenant, yml_file, default_flow_style=False)

    cfg = {}
    with open(file_path, "r") as file:
        cfg = yaml.load(file, Loader=yaml.BaseLoader)

    #Parse cfg for tenant names and create tokens for each tenant
    tenant_sessions = []
    for tenant in cfg:
        uname = cfg[tenant]['uname']
        passwd = cfg[tenant]['passwd']
        api_url = cfg[tenant]['url']

        tenant_sessions.append(CWPSessionManager(tenant, api_url, uname=uname, passwd=passwd, logger=logger))

    try:   
        return tenant_sessions[0]
    except:
        logger.error('Error - No credentials found. Exiting...')
        exit()

def load_multi_from_file(saas:bool, file_path='tenant_credentials.yml', logger=py_logger, num_tenants=-1) -> list:
    '''
    Reads config.yml and generates a Session object for the tenant
    Returns:
    Tenant Session object
    '''
    #Open and load config file
    if not os.path.exists(file_path):
        #Create credentials yml file
        __c_print('No credentials file found. Generating...', color='yellow')
        print()
        tenants = __get_credentials_from_user(num_tenants)
        with open(file_path, 'w') as yml_file:
            for tenant in tenants:
                yaml.dump(tenant, yml_file, default_flow_style=False)

    with open(file_path, "r") as file:
        cfg = yaml.load(file, Loader=yaml.BaseLoader)

    #Parse cfg for tenant names and create tokens for each tenant
    tenant_sessions = []
    for tenant in cfg:
        a_key = cfg[tenant]['access_key']
        s_key = cfg[tenant]['secret_key']
        api_url = cfg[tenant]['api_url']

        if saas == True:
            tenant_sessions.append(SaaSSessionManager(tenant, a_key, s_key, api_url, logger))
       

    return tenant_sessions

def load_from_file(file_path='tenant_credentials.yml', logger=py_logger) -> list:
    '''
    Reads config.yml and generates a Session object for the tenant
    Returns:
    Tenant Session object
    '''
    #Open and load config file
    if not os.path.exists(file_path):
        #Create credentials yml file
        __c_print('No credentials file found. Generating...', color='yellow')
        print()
        tenants = __get_credentials_from_user(1)
        with open(file_path, 'w') as yml_file: 
            for tenant in tenants:
                yaml.dump(tenant, yml_file, default_flow_style=False)

    with open(file_path, "r") as file:
        cfg = yaml.load(file, Loader=yaml.BaseLoader)

    #Parse cfg for tenant names and create tokens for each tenant
    tenant_sessions = []
    for tenant in cfg:
        a_key = cfg[tenant]['access_key']
        s_key = cfg[tenant]['secret_key']
        api_url = cfg[tenant]['api_url']

        tenant_sessions.append(SaaSSessionManager(tenant, a_key, s_key, api_url, logger))

    try:   
        return tenant_sessions[0]
    except:
        logger.error('Error - No credentials found. Exiting...')
        exit()

def load_from_env(logger=py_logger) -> object:
    error_exit = False

    name = 'Tenant'
    try:
        name = os.environ['PC_TENANT_NAME']
    except:
        logger.warning('Missing \'PC_TENANT_NAME\' environment variable. Using default name.')
    
    api_url = ''
    api = None
    try:
        api_url = os.environ['PC_TENANT_API']
        api = __validate_url(api_url)
    except:
        logger.error('Missing \'PC_TENANT_API\' environment variable.')
        error_exit = True

    a_key = None
    try:
        a_key = os.environ['PC_TENANT_A_KEY']
    except:
        logger.error('Missing \'PC_TENANT_A_KEY\' environment variable.')
        error_exit = True

    s_key = None
    try:
        s_key = os.environ['PC_TENANT_S_KEY']
    except:
        logger.error('Missing \'PC_TENANT_S_KEY\' environment variable.')
        error_exit = True

    if error_exit:
        logger.info('Missing required environment variables. Exiting...')
        exit()

    return SaaSSessionManager(name, a_key, s_key, api_url, logger)


def load_from_user(logger=py_logger, num_tenants=-1) -> list:
    tenant_sessions = []
    tenants = __get_credentials_from_user(num_tenants)
    for tenant in tenants:
        for key in tenant:
            name = key

            tenant_sessions.append(SaaSSessionManager(name, tenant[name]['access_key'], tenant[name]['secret_key'], tenant[name]['api_url'], logger))
            

    return tenant_sessions



