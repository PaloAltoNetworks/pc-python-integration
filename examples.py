#Uncomment a section to test

###INSTALLED FROM PYPI EXAMPLES
#Minimum setup-----------------------------------------------------------------
# from pcpi import session_loader

# session_manager = session.load_from_file()
# cspm_session = session_manager.create_cspm_session()

# res = cspm_session.request('GET', '/cloud')
# print(res.json())

#Recommended setup-------------------------------------------------------------
# from pcpi import session_loader
# import loguru

# session_manager = session.load_from_file(logger=loguru.logger)
# cspm_session = session_manager.create_cspm_session()

# res = cspm_session.request('GET', '/cloud')
# print(res.json())

#CSPM and CWP------------------------------------------------------------------
# from pcpi import session_loader
# import loguru

# session_manager = session.load_from_file(logger=loguru.logger)

# cspm_session = session_manager.create_cspm_session()
# cwp_session = session_manager.create_cwp_session()

# res = cspm_session.request('GET', '/cloud')
# print(res.json())

# print('--------------')

# res2 = cwp_session.request('GET', 'api/v1/credentials')
# print(res2.json())

#Session self healing----------------------------------------------------------
# from pcpi import session_loader
# import loguru

# session_man = session.load_from_file(logger=loguru.logger)

# cwp_session = session_man.create_cwp_session()
# cwp_session.cspm_token = 'asdasdasd'
# cwp_session.headers['Authorization'] = 'Bearer ' + 'sdfsdfsdfsdf'

# res = cwp_session.request('GET', 'api/v1/credentials')
# print(res.json())

# #Error and debugging output----------------------------------------------------------
# from pcpi import session_loader
# import loguru

# session_man = session.load_from_file(logger=loguru.logger)

# cwp_session = session_man.create_cwp_session()
# cwp_session.cspm_token = 'asdasdasd'
# cwp_session.headers['Authorization'] = 'Bearer ' + 'sdfsdfsdfsdf'

# res = cwp_session.request('GET', 'api/v9/credentials')


###LOCAL CLONED REPO EXAMPLES==================================================

#Minimum setup-----------------------------------------------------------------
# from src.pcpi import session_loader

# session_manager = session.load_from_file()
# cspm_session = session_manager.create_cspm_session()

# res = cspm_session.request('GET', '/cloud')
# print(res.json())

#Recommended setup-------------------------------------------------------------
# from src.pcpi import session_loader
# import loguru

# session_manager = session.load_from_file(logger=loguru.logger)
# cspm_session = session_manager.create_cspm_session()

# res = cspm_session.request('GET', '/cloud')
# print(res.json())

#CSPM and CWP------------------------------------------------------------------
# from src.pcpi import session_loader
# import loguru

# session_manager = session.load_from_file(logger=loguru.logger)

# cspm_session = session_manager.create_cspm_session()
# cwp_session = session_manager.create_cwp_session()

# res = cspm_session.request('GET', '/cloud')
# print(res.json())

# print('--------------')

# res2 = cwp_session.request('GET', 'api/v1/credentials')
# print(res2.json())

#Session self healing----------------------------------------------------------
# from src.pcpi import session_loader
# import loguru

# session_man = session.load_from_file(logger=loguru.logger)

# cwp_session = session_man.create_cwp_session()
# cwp_session.cspm_token = 'asdasdasd'
# cwp_session.headers['Authorization'] = 'Bearer ' + 'sdfsdfsdfsdf'

# res = cwp_session.request('GET', 'api/v1/credentials')
# print(res.json())

# #Error and debugging output----------------------------------------------------------
# from src.pcpi import session_loader
# import loguru

# session_man = session.load_from_file(logger=loguru.logger)

# cwp_session = session_man.create_cwp_session()
# cwp_session.cspm_token = 'asdasdasd'
# cwp_session.headers['Authorization'] = 'Bearer ' + 'sdfsdfsdfsdf'

# res = cwp_session.request('GET', 'api/v9/credentials')



