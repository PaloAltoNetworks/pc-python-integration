# Prisma Cloud Python Integration - PCPI

## Python3 toolkit for Prisma Cloud APIs

# Disclaimer

This tool is supported under "best effort" policies. Please see SUPPORT.md for details.

# Installation

```pip3 install pcpi```

# Setup

# Use

## Session Loaders

The session loader is a module that has functions for loading Prisma Cloud credentials from a file, environment variables, or from the user into your program. This ensures you get your script up and running as quickly as possible.

The session_loader function returns a session manager that is ready to be used to create a CSPM, CWP, or an On-Prem CWP session. The session manager is used to create the Prisma Cloud session object that you will be using to make API calls.

**Examples**

SaaS Examples
```python
from loguru import logger
loguru_logger = logger

from pcpi import session_loader

#Defaults to a file named 'tenant_credentials.yml'
session_manager_default = session_loader.load_from_file(logger=loguru_logger)

#File must be a yaml (.yml) file. 
#If a file that does not exist is specified, the script will build one.
session_manager = session_loader.load_from_file(file_path='~/secrets/my_secrets.yml')

cspm_session = session_manager.create_cspm_session()
cwp_session = session_manager.create_cwp_session()

response = cspm_session.request('GET', '/cloud')

print(response.json())
```

```python
from pcpi import session_loader

session_manager = session_loader.load_from_env()
```

```python
from pcpi import session_loader

session_manager = session_loader.load_from_user()
```

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
    api_url='https://api.prismacloud.io',
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

## Beta release 8/11/2022
**Patch Notes**
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