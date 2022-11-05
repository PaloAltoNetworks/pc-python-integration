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

# Quick Start

1) Create a file with a text editor of your choice (I recommend VS Code). Name this file **script.py**
2) Open the file and add these lines:
```python
from pcpi import session_loader
session_man = session_loader.load_from_file()
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
session_loader.load_from_file()
session_loader.load_from_env()
session_loader.load_from_user()
session_loader.onprem_load_from_file()
session_loader.onprem_load_from_env()
session_loader.onprem_load_from_user()

#-- SESSION LOADER ARGUMENTS --
#Session loader arguments are all optional
#logger -- exclude to use default pylogger config or create a py logger object and pass that in for the logger value. Can also use a loguru logger object
#file_path -- Path to credentials file. File will be created at the path specified. Exclude argument to use default path.
session_loader.load_from_file(logger=, file_path='')

#-- SESSION MANAGERS --
#Session loader returns a session manager object
session_manager = session_loader.load_from_env()
onprem_session_manager = session_loader.onprem_load_from_env()

#Session managers return session objects
#-- SESSION MANAGER FUNCTIONS --
cspm_session = session_manager.create_cspm_session()
cwp_session = session_manager.create_cwp_session()
onprem_cwp_session = onprem_session_manager.create_cwp_session()

#-- SESSION FUNCTION --
#Session objects are used to make API requests
cspm_session.request('', '', json={}, params={})

#-- SESSION REQUEST ARGUMENTS --
#method - required - the http verb used in the request
#endpoint_url - required - the path of the API endpoint
#json - optional - the payload for the API call - converts python dictionaries into json automatically
#data - optional - payload alterative that does not convert python dictionaries into json
#params - optional - query string parameters can be included as a python dictionary
```

# Prisma Cloud Python Integration Documentation and Examples

## Session Loaders

The session loader is a module that has functions for loading Prisma Cloud credentials from a file, environment variables, or from the user into your program. This ensures you get your script up and running as quickly as possible.

The session_loader function returns a session manager that is ready to be used to create a CSPM, CWP, or an On-Prem CWP session. The session manager is used to create the Prisma Cloud session object that you will be using to make API calls.

**Examples**

SaaS Examples
```python
from loguru import logger
loguru_logger = logger

from pcpi import session_loader

#--DEFAULT OPTION--
#Defaults to a file named 'tenant_credentials.yml'
session_manager_default = session_loader.load_from_file(logger=loguru_logger)

#--CUSTOM OPTION--
#File must be a yaml (.yml) file. 
#If a file that does not exist is specified, the script will build one. Only creates end file, not directory structure. That setup is up to you.
session_manager = session_loader.load_from_file(file_path='~/secrets/my_secrets.yml')

cspm_session = session_manager.create_cspm_session()
cwp_session = session_manager.create_cwp_session()

response = cspm_session.request('GET', '/cloud')

print(response.json())
```

For SaaS CSPM and CWP

```python
from pcpi import session_loader

session_manager = session_loader.load_from_env()
```

```python
from pcpi import session_loader

session_manager = session_loader.load_from_user()
```

For CWP Self Hosted

```python
from pcpi import session_loader

session_manager = session_loader.onprem_load_from_file()
session_manager = session_loader.onprem_load_from_env()
session_manager = session_loader.onprem_load_from_user()

session_manager.create_cwp_session()
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

#Defaults to a file named 'tenant_credentials.yml'
session_manager_default = session_loader.load_from_file(logger=loguru_logger)

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

response = cspm_session.request('POST', '/cloud/aws', json=payload, params=query_string)
print(response.status_code)
```

## Logging

Two logging libraries are supported by PCPI. The built in Python logging library (used by default) and Loguru.
Loguru is strongly recommended but it is an additional dependency that you may not want.

**EXAMPLES**

```python
#Minimum setup
from pcpi import session_loader

session_manager = session.load_from_file()
cspm_session = session_manager.create_cspm_session()

res = cspm_session.request('GET', '/cloud')
print(res.json())

#Recommended setup
from pcpi import session_loader
import loguru

session_manager = session.load_from_file(logger=loguru.logger)
cspm_session = session_manager.create_cspm_session()

res = cspm_session.request('GET', '/cloud')
print(res.json())
```

# Function Reference

# Announcements

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