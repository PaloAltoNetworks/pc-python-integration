# Prisma Cloud Python Integration - PCPI

## Python3 toolkit for Prisma Cloud APIs

# Disclaimer

This tool is supported under "best effort" policies. Please see SUPPORT.md for details.

# Announcements

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

# Installation

```pip3 install pcpi```

# Setup

# Use

## Session Loaders

The session loader is a module that has functions for loading Prisma Cloud credentials from a file, environment variables, or from the user into your program. This ensures you get your script up and running as quickly as possible.

The session_loader function returns a session manager that is ready to be used to create a CSPM, CWP, or an On-Prem CWP session. The session manager is used to create the Prisma Cloud session object that you will be using to make API calls.

### Examples

SaaS Examples
```python
from pcpi import session_loader

#Defaults to a file named 'tenant_credentials.yml'
session_manager_default = session_loader.load_from_file()

#File must be a yaml (.yml) file. If a file that does not exist is specified, the script will build one.
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

## Requests



