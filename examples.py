#Uncomment a section to test

###INSTALLED FROM PYPI EXAMPLES
#Minimum setup-----------------------------------------------------------------
# from pcpi import session_loader

# session_managers = session_loader.load_config()
# session_manager = session_managers[0]
# cspm_session = session_manager.create_cspm_session()

# res = cspm_session.request('GET', '/cloud')
# print(res.json())

#Recommended setup-------------------------------------------------------------
# from pcpi import session_loader
# import loguru

# session_managers = session_loader.load_config(logger=loguru.logger)
# session_manager = session_managers[0]
# cspm_session = session_manager.create_cspm_session()

# res = cspm_session.request('GET', '/cloud')
# print(res.json())

#CSPM and CWP------------------------------------------------------------------
# from pcpi import session_loader
# import loguru

# session_managers = session_loader.load_config(logger=loguru.logger)
# session_manager = session_managers[0]

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

# session_managers = session_loader.load_config(logger=loguru.logger)
# session_manager = session_managers[0]

# cwp_session = session_manager.create_cwp_session()
# cwp_session.cspm_token = 'asdasdasd'
# cwp_session.headers['Authorization'] = 'Bearer ' + 'sdfsdfsdfsdf'

# res = cwp_session.request('GET', 'api/v1/credentials')
# print(res.json())

#Error and debugging output----------------------------------------------------------
# from pcpi import session_loader
# import loguru

# session_managers = session_loader.load_config(logger=loguru.logger)
# session_manager = session_managers[0]

# cwp_session = session_manager.create_cwp_session()
# cwp_session.cspm_token = 'asdasdasd'
# cwp_session.headers['Authorization'] = 'Bearer ' + 'sdfsdfsdfsdf'

# res = cwp_session.request('GET', 'api/v9/credentials')


###LOCAL CLONED REPO EXAMPLES==================================================

#Minimum setup-----------------------------------------------------------------
# from src.pcpi import session_loader

# session_managers = session_loader.load_config()
# session_manager = session_managers[0]
# cspm_session = session_manager.create_cspm_session()

# res = cspm_session.request('GET', '/cloud')
# print(res.json())

#Recommended setup-------------------------------------------------------------
# from src.pcpi import session_loader
# import loguru

# session_managers = session_loader.load_config(logger=loguru.logger)
# session_manager = session_managers[0]
# cspm_session = session_manager.create_cspm_session()

# res = cspm_session.request('GET', '/cloud')
# print(res.json())

#CSPM and CWP------------------------------------------------------------------
# from src.pcpi import session_loader
# import loguru

# session_managers = session_loader.load_config(logger=loguru.logger)
# session_manager = session_managers[0]

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

# session_managers = session_loader.load_config(logger=loguru.logger)
# session_manager = session_managers[0]

# cwp_session = session_manager.create_cwp_session()
# cwp_session.cspm_token = 'asdasdasd'
# cwp_session.headers['Authorization'] = 'Bearer ' + 'sdfsdfsdfsdf'

# res = cwp_session.request('GET', 'api/v1/credentials')
# print(res.json())

# #Error and debugging output----------------------------------------------------------
# from src.pcpi import session_loader
# import loguru

# session_managers = session_loader.load_config(logger=loguru.logger)
# session_manager = session_managers[0]

# cwp_session = session_manager.create_cwp_session()
# cwp_session.cspm_token = 'asdasdasd'
# cwp_session.headers['Authorization'] = 'Bearer ' + 'sdfsdfsdfsdf'

# res = cwp_session.request('GET', 'api/v9/credentials')


#Heuristic Search--------------------------------------------------------------
# #Change RQL query as needed
# query = "config from cloud.resource where resource.status = Active AND api.name = 'aws-ec2-describe-instances'"

# #Payload can use absolute time range or relative time range. Examples are given of both time ranges.
# payload = {
#     "query": query,
#     "timeRange": {
#         "relativeTimeType": "BACKWARD",
#         "type": "relative",
#         "value": {
#             "amount": 24,
#             "unit": "hour"
#         }
#     },
# }


# # # Option 1 PCPI paginates automatically and returns JSON data as one chunk.
# # json_data = cspm_session.config_search_request(payload)

# # #Dump json to file
# # with open('totalDataRETURNED.json', 'w') as outfile:
# #     json.dump(json_data, outfile)

# #---------------------------

# # Option 2 PCPI paginates automatically but now you pass in a custom function that controls what to do with each page of data.
# def dump_data(details, data, counter, total_rows):
#     if counter == 0:
#         with open(f'detailsOut.json', 'w') as outfile:
#             json.dump(details, outfile)

#     with open(f'temp/dataOut{counter}.json', 'w') as outfile:
#         json.dump(data, outfile)

# total_rows = cspm_session.config_search_request_function(payload, dump_data)

# print(f'Got {total_rows} Total Rows')
