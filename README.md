# Prisma Cloud Python Integration - PCPI

## Python3 toolkit for Prisma Cloud APIs

# Disclaimer

This tool is supported under "best effort" policies. Please see SUPPORT.md for details.

# Installation
This tool requires Python3. Please visit https://www.python.org/downloads/ for Python3 installation guides.

Depending on your environment, you may have to install the pcpi library in a different way.

**This tool only needs to be installed in ONE of these ways, do not run all of these commands.**

Run one of the following commands in a terminal/command prompt:

Mac/Linux
- ```pip3 install pcpi```
- ```python3 -m pip install pcpi```
- ```pip install pcpi```

Windows
- ```py -m pip install pcpi```
- ```python -m pip install pcpi```
- ```pip install pcpi```
- ```pip3 install pcpi```
- ```python3 -m pip install pcpi```

To update an existing installation, ad the '--upgrade' flag to the pip command. EX:
- ```pip3 install --upgrade pcpi```

# Quick Start

1) Create a file with a text editor of your choice (I recommend VS Code). Name this file **script.py**
2) Open the file and add these lines:
```python
from pcpi import session_loader
#load_config will create a config file if one does not exist. Default path is ~./prismacloud/credentails.json
session_managers = session_loader.load_config()
#load_config returns a list of session_manager objects. If only one is needed, index the list at position 0 
# to get the first and only session_manager.
#load_config() will create a credential file for you if the default path or the specified path does not exist.
#load_config() accepts credentials for SaaS and Self hosted Prisma Cloud and smartly returns either a SaaS session manager or
# an On-Prem session manager.
session_man = session_managers[0]
#If you supplied credentials for Prisma Cloud SaaS, you can create a CSPM Session Or a CWP Session.
#create_cspm_session(), create_cwp_session()
#If you supplied credentials for Prisma Cloud Self Hosted/On-prem, you will only be able to create CWP sessions.
#create_cwp_session()
cspm_session = session_man.create_cspm_session()

res = cspm_session.request('GET', '/cloud')

print(res.json())
```
3) Run the script by opening a terminal/command prompt, navigating to your directory/folder then using the Python command and specifying the name of your Python script. You may have to use a different name for the Python program depending on your environment.

Mac/Linux
```
python3 script.py
```
Windows
```
py script.py
```
4) When running this script for the first time, the pcpi library will prompt you for your Prisma Cloud credentials. Follow the prompts and if all goes well, you should see some ```SUCCESS``` messages being logged to your terminal. If you see ```ERROR```s, then you may have to disable any VPNs you are connected too and you need to ensure you have valid Prisma Cloud credentials.

5) This example script calls the ```/cloud``` endpoint. After this script runs, you should see data from your tenant about cloud accounts in JSON format.

# Scripting Setup Guide
1) Import pcpi into your python project

2) Create a session manager directly or by using a session loader  
2a) Session Loader arguments are all optional.  
2b) Specify a file path, if file_path variable is excluded, the default credential path will be used.  
2c) If the credentials file does not exist, the script will set it up for you at the specified or default file path

3) Create a CSPM or CWP session by using the session manager.

4) Use the created session object to make API requests

5) Run the script
```
python3 <yourscriptname>.py
```

```python
import pcpi

session_loader = pcpi.session_loader

#-- SESSION LOADER FUNCTIONS --
session_loader.load_config()
session_loader.load_config_env()
session_loader.load_config_user()

# Each session loader accepts credentials for SaaS and Self hosted Prisma Cloud and smartly returns either a SaaS session manager or
# an On-Prem session manager.

#-- SESSION LOADER ARGUMENTS --
#--Session loader arguments are all optional--

# load_config()
#file_path -- Path to credentials file. File will be created at the path specified. 
# Exclude argument to use default path.
#num_tenants -- Number of tenant configurations that will be included in the config JSON file. 
# Only applies when a config file is being created.
#min_tenants -- Minimum number of tenants to be included in the config file. 
# User setting up config file will be prompted to continue after minimum
# number of tenants have been reached
#You can not use num_tenants and min_tenants at the same time. Only include one or the other.
#logger -- exclude to use default pylogger config or create a py logger object and pass that in for the logger value. 
# Can also use a loguru logger object
session_loader.load_config(file_path='', num_tenants=-1, min_tenants=-1, logger=logger) # returns session manager list

# load_config_user()
#num_tenants -- Number of tenant configurations that will be included in the config JSON file. 
# Only applies when a config file is being created.
#min_tenants -- Minimum number of tenants to be included in the config file. 
# User setting up config file will be prompted to continue after minimum
# number of tenants have been reached
#You can not use num_tenants and min_tenants at the same time. Only include one or the other.
#logger -- exclude to use default pylogger config or create a py logger object and pass that in for the logger value. 
# Can also use a loguru logger object
load_config_user(num_tenants=-1, min_tenants=-1, logger=py_logger) # returns session manager list

# load_config_env()
#prisma_name='PRISMA_PCPI_NAME' -- overwrites the default env var name for the 'name' Prisma Credential
#identifier_name='PRISMA_PCPI_ID' -- overwrites the default env var name for the 'ID' Prisma Credential
#secret_name='PRISMA_PCPI_SECRET' -- overwrites the default env var name for the 'secret' Prisma Credential 
#api_url_name='PRISMA_PCPI_URL' -- overwrites the default env var name for the 'api_url' Prisma Credential
#verify_name='PRISMA_PCPI_VERIFY', -- overwrites the default env var name for the 'verify' Prisma Credential
#logger -- exclude to use default pylogger config or create a py logger object and pass that in for the logger value. 
# Can also use a loguru logger object
load_config_env(prisma_name='PRISMA_PCPI_NAME', identifier_name='PRISMA_PCPI_ID', secret_name='PRISMA_PCPI_SECRET', 
                api_url_name='PRISMA_PCPI_URL', verify_name='PRISMA_PCPI_VERIFY',  project_flag_name='PRISMA_PCPI_PROJECT_FLAG', logger=py_logger) # returns single session manager

#-- SESSION MANAGERS --
#Session loader returns a list of session managers
session_managers = session_loader.load_config() 
#load_config() returns either a SaaS session manager or On-Prem session manager based on credentials used, namely the api url.
my_session_manager = session_managers[0]
my_onprem_session_manager = session_managers[1]

#Session managers return session objects
#-- SESSION MANAGER FUNCTIONS --
cspm_session = my_session_manager.create_cspm_session()
cwp_session = my_session_manager.create_cwp_session()
onprem_cwp_session = my_onprem_session_manager.create_cwp_session()

#-- SESSION FUNCTION --
#Session objects are used to make API requests
cspm_session.request('GET', '<api_endpoint>', json={}, params={}, verify=True)
cwp_session.request( 'POST', '<api_endpoint>', json={}, params={}, verify=True)

#-- SESSION REQUEST ARGUMENTS --
#method - position 1 - required - the http verb used in the request
#endpoint_url - position 2 - required - the path of the API endpoint
#json - optional - the payload for the API call - converts python dictionaries into json automatically
#data - optional - payload alterative that does not convert python dictionaries into json
#params - optional - query string parameters can be included as a python dictionary
#verify - optional - True, False, or path to certificate file. Disables or overwrites HTTPS Certificate verification.
```

# Prisma Cloud Python Integration Documentation and Examples

## Session Loaders

The session loader is a module that has functions for loading Prisma Cloud credentials from a file, environment variables, or from the user into your program. This ensures you get your script up and running as quickly as possible.

The session loader module has functions that return a session manager or session manager list that is used to create a CSPM, CWP, or an On-Prem CWP session. The session manager is used to create the Prisma Cloud session object that you will be using to make API calls.

**Examples**

SaaS Examples
```python
from loguru import logger
loguru_logger = logger

from pcpi import session_loader

#--DEFAULT OPTION--
#Defaults to a file named '~./prismacloud/credentials.json'
session_manager_default = session_loader.load_config(logger=loguru_logger)

#--CUSTOM OPTION--
#File must be a json file 
#If a file that does not exist is specified, the script will build one. Only creates end file, not directory structure. That setup is up to you.
#If using default file path, load_config() will create the ~/.prismacloud/credentials.json file structure.
session_managers = session_loader.load_config(file_path='~/secrets/my_secrets.json')
session_manager = session_managers[0]

cspm_session = session_manager.create_cspm_session()
cwp_session = session_manager.create_cwp_session()

response = cspm_session.request('GET', '/cloud')

print(response.json())
```

For SaaS CSPM and CWP and Self Hosted/On-Prem CWP

```python
from pcpi import session_loader

session_manager = session_loader.load_config_env() #only returns a single session_manager object
```

```python
from pcpi import session_loader

session_managers = session_loader.load_config_user()
session_manager = session_managers[0]
```

## Session Managers

If you want to take control on how credentials are stored/loaded into your scripts, use the session managers directly and skip the session loader module. Session manager objects directly accept Prisma Cloud credentials into the object constructor. 

This still creates the same Prisma Cloud session object that you use for API requests.

**EXAMPLES**

```python
from pcpi import saas_session_manager
import logging

py_logger = logging.getLogger()
py_logger.setLevel(10)

session_manager = saas_session_manager.SaaSSessionManager(
    tenant_name='My PC Tenant',
    a_key='xxxxxxxxxxxxxxxxxxxxxxxxxx',
    s_key='xxxxxxxxxxxxxxxxxxxxxxxxxx',
    api_url='https://api.prismacloud.io',
    logger=py_logger
)

cspm_session = session_manager.create_cspm_session()
cwp_session = session_manager.create_cwp_session()
```

```python
from pcpi import onprem_session_manager
import logging

py_logger = logging.getLogger()
py_logger.setLevel(10)

session_manager = onprem_session_manager.CWPSessionManager(
    tenant_name='My PC Tenant',
    uname='xxxxxxxxxxxxxxxxxxxxxxxxxx',
    passwd='xxxxxxxxxxxxxxxxxxxxxxxxxx',
    api_url='https://<yourselfhostedurl>',
    logger=py_logger
)

onprem_cwp_session = session_manager.create_cwp_session()
```

## Requests

The Prisma Cloud Python Integration uses the Python3 Requests library to make API calls. The Prisma Cloud Session object that this tool provides has a wrapper function for API calls using the requests function from Requests. The main difference is that this tool handles the 'headers' section of the request for you. The remaining fields can be used just like you would use the requests library [requests.request](https://requests.readthedocs.io/en/latest/api/#requests.request).

**EXAMPLES**

```python
from loguru import logger
loguru_logger = logger

from pcpi import session_loader

#Default config file will be created at '~/.prismacloud/credentials.json'
session_managers = session_loader.load_config(logger=loguru_logger)
session_manager = session_managers[0]

cspm_session = session_manager.create_cspm_session()

response = cspm_session.request('GET', '/cloud')
print(response.json())

payload = {
    "accountId":"xxxxx",
    "accountType":"account",
    "enabled":True,
    "externalId":"xxxxxx",
    "groupIds":["xxxxx"],
    "name":"Name",
    "protectionMode":"MONITOR",
    "roleArn":"xxxxxxx",
    "storageScanEnabled":False,
    "vulnerabilityAssessmentEnabled":False
}

query_string = {"skipStatusChecks":1}

response = cspm_session.request('POST', '/cloud/aws', json=payload, params=query_string, verify='path_to_cert.pem')
print(response.status_code)
```

## Logging

Two logging libraries are supported by PCPI. The built in Python logging library (used by default) and Loguru.
Loguru is strongly recommended but it is an additional dependency that you may not want.

**EXAMPLES**

```python
#Minimum setup
from pcpi import session_loader

#Default pylogger is used if none is specified
session_managers = session_loader.load_config()
session_manager = session_managers[0]

cspm_session = session_manager.create_cspm_session()

res = cspm_session.request('GET', '/cloud')
print(res.json())

#Recommended setup
from pcpi import session_loader
import loguru

#Check out loguru docs for details on configuration options.

session_managers = session_loader.load_config(logger=loguru.logger)
session_manager = session_managers[0]
cspm_session = session_manager.create_cspm_session()

res = cspm_session.request('GET', '/cloud')
print(res.json())

#Custom Setup
#If you wish to change the amount of logging output seen in the terminal, or output logs to a file,
# you can overwrite the default logger with a customer pylogger object or a customer loguru object.
from pcpi import session_loader
import logging

logging.basicConfig()
py_logger = logging.getLogger("pcpi")
py_logger.setLevel(100) #turns off logging since no default logs have a level of over 50

session_managers = session_loader.load_config(logger=py_logger)
session_manager = session_managers[0]
cspm_session = session_manager.create_cspm_session()

res = cspm_session.request('GET', '/cloud')
print(res.json())

```

# Function Reference

# Announcements

## Stable release 12/6/2022
**News**
JSON files are replacing yaml files for credential management.
Credential files now cross compatible with [Prisma Cloud API Python](https://github.com/PaloAltoNetworks/prismacloud-api-python).
- New Session Loaders that handle credential management for you
- - load_config(), load_config_env(), and load_config_user() introduced to replace other session managers
- - JSON files now used instead of yaml
- - Default Credential path changes to ~/.prismacloud/credentials.json
- - No longer requires separate credential files for SaaS and On Prem

**Patch Notes**
- Various bug fixes and stability improvements

## Stable release 8/11/2022
**News**
Current version is considered stable as known bugs have been fixed.
Documentation is still a work in progress.
Not all features have been implemented yet.
Current Features:
- SaaS CSPM, SaaS CWP, and On-prem CWP session/JWT management
- - Generates JWT tokens as needed and uses them for full valid duration
- - Progressive back-off algorithm to avoid API DOS protections
- - Automatic retires on error codes
- - Detailed logging support through Python Logging and Loguru modules
- Session Loaders that handle credential management for you to jump start your script development.
- - Supports loading credentials from a file, from environment variables, and directly from the user as a series of prompts.
- - Will build out credential files for you, just specify desired file path
- - Helpful debug messages on missing values for environment variables
- Session Managers that intelligently handle SaaS and On-Prem sessions
- - Reuses existing CSPM SaaS session when making SaaS CWP API calls
- - Direct access to session managers to enable you to handle credentials as you see fit

**Patch Notes**
- On-prem support
- Fixed Keyboard Interrupt exception handling
- Fixed default logger bug

## Beta release 9/15/2022
**Patch Notes**
- Renamed module
- - session -> session_loader

**Known bugs:**
- Default logging library is missing output. Using loguru solves this in the meantime.

## Beta release 9/14/2022
**Patch Notes**
- Renamed repo to match package name
- Reorganized repository to be compatible with PyPI package structure
- Examples file changed to support new file structure
- Package published to PyPi for easy use and updates

**Known bugs:**
- Default logging library is missing output. Using loguru solves this in the meantime.

## Beta release 09/12/2022
**Patch notes**
- Modules and function name changes
- - pc_session -> session
- Spelling and typo fixes
- Small bug fixes

API Toolkit python package is scheduled for release on 09/15/2022.
With this release there will be a freeze on module/function names.
Until then names are subject to change.

**Known bugs:**
- Default logging library is missing output. Using loguru solves this in the meantime.

## Beta release 09/01/2022
Self Hosted CWP is not yet supported, coming soon.

No documentation yet but coming soon. Please refer to "examples.py" in the meantime.

**Known bugs:**
- Default logging library is missing output. Using loguru solves this in the meantime.
