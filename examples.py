#Uncomment a section to test


#Minimum setup-----------------------------------------------------------------
# import pc_session

# session_manager = pc_session.load_from_file(saas=True)
# cspm_session = session_manager.create_cspm_session()

# res = cspm_session.request('GET', '/cloud')
# print(res.json())

#Reccomended setup-------------------------------------------------------------
# import pc_session
# import loguru

# session_manager = pc_session.load_from_file(saas=True,logger=loguru.logger)
# cspm_session = session_manager.create_cspm_session()

# res = cspm_session.request('GET', '/cloud')
# print(res.json())

#CSPM and CWP------------------------------------------------------------------
# import pc_session
# import loguru

# session_manager = pc_session.load_from_file(saas=True,logger=loguru.logger)

# cspm_session = session_manager.create_cspm_session()
# cwp_session = session_manager.create_cwp_session()

# res = cspm_session.request('GET', '/cloud')
# print(res.json())

# print('--------------')

# res2 = cwp_session.request('GET', 'api/v1/credentials')
# print(res2.json())

#Session self healing----------------------------------------------------------
# import pc_session
# import loguru

# session_man = pc_session.load_from_file(saas=True, logger=loguru.logger)

# cwp_session = session_man.create_cwp_session()
# cwp_session.cspm_token = 'asdasdasd'
# cwp_session.headers['Authorization'] = 'Bearer ' + 'sdfsdfsdfsdf'

# res = cwp_session.request('GET', 'api/v1/credentials')
# print(res.json())

# #Error and debugging output----------------------------------------------------------
# import pc_session
# import loguru

# session_man = pc_session.load_from_file(saas=True, logger=loguru.logger)

# cwp_session = session_man.create_cwp_session()
# cwp_session.cspm_token = 'asdasdasd'
# cwp_session.headers['Authorization'] = 'Bearer ' + 'sdfsdfsdfsdf'

# res = cwp_session.request('GET', 'api/v9/credentials')



