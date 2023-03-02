#Standard Library
import time

import json as json_lib

#installed
import requests

from urllib3.exceptions import InsecureRequestWarning

class Session:
    def __init__(self,logger):
        """
        Initializes a Prisma Cloud API Session Manager.

        Keyword Arguments:
        logger - optional logger, either pylib logger or loguru
        """
        self.retries = 20
        self.retry_statuses = [401, 425, 429, 500, 502, 503, 504]
        self.retry_delay_statuses = [429, 500, 502, 503, 504]
        self.success_status = [200,201,202,203,204,205,206]
        self.expired_code = 401
        self.retry_timer = 0
        self.retry_timer_max = 32
        self.token_time = 360

        self.empty_res = ''

        self.u_count = 1
        self.unknown_error_max = 5

        self.logger = logger

#==============================================================================
    def _api_login_wrapper(self):
        if self.verify == False:
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

        res = self.empty_res
        while res == self.empty_res and self.u_count < self.unknown_error_max:
            try:
                res, time_completed = self._api_login()

                retries = 0
                encountered_401 = False
                while res.status_code in self.retry_statuses and retries < self.retries:
                    if res.status_code in self.retry_delay_statuses:
                        self.logger.warning(f'FAILED {res.status_code} - {time_completed} seconds')
                        
                        #Increase timer when ever encounted to slow script execution.
                        if self.retry_timer == 0:
                            self.retry_timer = 1
                        else:
                            self.retry_timer = self.retry_timer*2
                            if self.retry_timer >= self.retry_timer_max:
                                self.retry_timer = self.retry_timer_max

                        self.logger.warning(f'Waiting {self.retry_timer} seconds')
                        time.sleep(self.retry_timer)
                        self.logger.warning('Increasing wait time.')

                    elif res.status_code == self.expired_code:
                        if encountered_401 == True:
                            self.logger.error('ERROR - Can not perform API operations')
                            self.logger.warning('Steps to troubleshoot: ')
                            self.logger.warning('1) Ensure Access Key has proper permission.')
                            self.logger.warning('2) Ensure Prisma Cloud license is valid.')
                            self.logger.warning('3) If using a CWPP Project, ensure project name is valid in credential configurations.')
                            exit()

                        self._expired_login()
                        encountered_401 = True
                    else:
                        code = "NO_CODE"
                        try:
                            code = res.status_code
                        except:
                            pass
                        self.logger.error(f'FAILED {code} - {time_completed} seconds')
                        self.logger.error('ERROR Logging In. JWT not generated.')
                        self.logger.warning('RESPONSE:')
                        self.logger.info(res)
                        self.logger.warning('RESPONSE URL:')
                        self.logger.info(res.url)
                        self.logger.warning('RESPONSE TEXT:')
                        self.logger.info(res.text)

                    
                    res, time_completed = self._api_login()

                    retries +=1
                
                if retries == self.retries:
                    self.logger.error('ERROR. Max retires exceeded on API Login. Exiting...')
                    exit()

                #Update token and headers
                token = res.json().get('token')
                self.token = token
                new_headers = self.headers
                new_headers[self.auth_key] = self.auth_style + token
                self.headers = new_headers

                try:
                    self.logger.success(f'SUCCESS - {time_completed} seconds')
                except:
                    self.logger.info(f'SUCCESS - {time_completed} seconds')

                self.u_count = 1
                return token

            except KeyboardInterrupt:
                self.logger.error('Keyboard Interrupt. Exiting...')
                exit()
            except Exception as e:
                self.logger.error(e)
                self.logger.error(f'UNKNOWN ERROR - API login. Retrying... {self.u_count} of {self.unknown_error_max}')
                self.u_count += 1
                self.logger.warning('Steps to troubleshoot: ')
                self.logger.warning('1) Disable any VPNs.')
                self.logger.warning('2) Ensure API base URL is correct.')
                time.sleep(1)

    def _api_refresh_wrapper(self):
        res = self.empty_res

        refresh_func = getattr(self, "_api_refresh", None)
        if not callable(refresh_func):
            return self._api_login_wrapper()
        else:
            while res == self.empty_res and self.u_count < self.unknown_error_max:
                try:
                    res, time_completed = self._api_refresh()

                    retries = 0
                    while res.status_code in self.retry_statuses and retries < self.retries:
                        if res.status_code in self.retry_delay_statuses:
                            self.logger.warning(f'CODE {res.status_code} - {time_completed} seconds')
                            self.logger.warning(f'HEADERS: {res.headers}')
                            #Increase timer when ever encounter to slow script execution.
                            if self.retry_timer == 0:
                                self.retry_timer = 1
                            else:
                                self.retry_timer = self.retry_timer*2
                                if self.retry_timer >= self.retry_timer_max:
                                    self.retry_timer = self.retry_timer_max

                            self.logger.warning(f'Waiting {self.retry_timer} seconds')
                            time.sleep(self.retry_timer)
                            self.logger.warning('Increasing wait time.')

                        elif res.status_code == self.expired_code:
                            self.logger.error(f'FAILED {self.expired_code} - {time_completed} seconds')
                            self.logger.warning('Session expired. Generating new Token')
                            self._api_login_wrapper()
                            return
                        else:
                            code = "NO_CODE"
                            try:
                                code = res.status_code
                            except:
                                pass
                            self.logger.error(f'FAILED {code} - {time_completed} seconds')
                            self.logger.error('ERROR Refreshing Token.')
                            self.logger.warning('RESPONSE:')
                            self.logger.info(res)
                            self.logger.warning('RESPONSE URL:')
                            self.logger.info(res.url)
                            self.logger.warning('RESPONSE TEXT:')
                            self.logger.info(res.text)
                        
                        res, time_completed = self._api_refresh()

                        retries +=1
                    
                    if retries == self.retries:
                        self.logger.error('ERROR. Max retires exceeded on JWT refresh. Exiting...')
                        exit()

                    #Update token and headers
                    token = res.json().get('token')
                    self.token = token
                    new_headers = self.headers
                    new_headers[self.auth_key] = self.auth_style + token
                    self.headers = new_headers

                    try:
                        self.logger.success(f'SUCCESS - {time_completed} seconds')
                    except:
                        self.logger.info(f'SUCCESS - {time_completed} seconds')

                    self.u_count = 1

                    return

                except KeyboardInterrupt:
                    self.logger.error('Keyboard Interrupt. Exiting...')
                    exit()
                except Exception as e:
                    self.logger.error(e)
                    self.logger.error(f'UNKNOWN ERROR - API refresh. Retrying... {self.u_count} of {self.unknown_error_max}')
                    self.u_count += 1
                    self.logger.warning('Steps to troubleshoot: ')
                    self.logger.warning('1) Disable any VPNs.')
                    self.logger.warning('2) Ensure API base URL is correct.')
                    time.sleep(1)


#==============================================================================
    def __api_call_wrapper(self, method: str, url: str, json: dict=None, data: dict=None, params: dict=None, verify=True, acceptCsv=False, redlock_ignore: list=None, status_ignore: list=[], custom_log='', custom_error_message=''):
        """
        A wrapper around all API calls that handles token generation, retrying
        requests and API error console output logging.
        Keyword Arguments:
        method -- Request method/type. Ex: POST or GET
        url -- Full API request URL
        data -- Body of the request in a json compatible format
        params -- Queries for the API request
        Returns:
        Respose from API call.
        """
        res = self.empty_res
        while res == self.empty_res and self.u_count < self.unknown_error_max:
            try:
                if time.time() - self.token_time_stamp >= self.token_time:
                    self.logger.warning('Session Refresh Timer - Generating new Token')
                    self._api_refresh_wrapper()

                self.logger.debug(f'{url}')
                res,time_completed = self.__request_wrapper(method, url, headers=self.headers, json=json, data=data, params=params, verify=verify, acceptCsv=acceptCsv)
                
                if res.status_code in self.success_status or res.status_code in status_ignore:
                    log_message = ''
                    if custom_log:
                        log_message = ' - ' + custom_log

                    try:
                        self.logger.success(f'SUCCESS - {time_completed} seconds{log_message}')
                    except:
                        self.logger.info(f'SUCCESS - {time_completed} seconds{log_message}')
                    return res

                retries = 0
                encountered_401 = False
                while res.status_code in self.retry_statuses and retries < self.retries:
                    #If we get a 429 code, sleep for a doubling amount of time.
                    if res.status_code in self.retry_delay_statuses:
                        error_msg = ''
                        log_message = ''
                        if custom_error_message:
                            error_msg = " - " + custom_error_message
                        if custom_log:
                            log_message = ' - ' + custom_log

                        self.logger.warning(f'FAILED {res.status_code} - {time_completed} seconds{log_message}{error_msg}')
                        #Wait for retry timer
                        if self.retry_timer > 0:
                            self.logger.warning(f'Waiting {self.retry_timer} seconds')
                            time.sleep(self.retry_timer)

                        self.logger.warning('Increasing wait time')
                        #Increase timer when ever wait status encounted to slow script execution.
                        if self.retry_timer == 0:
                            self.retry_timer = 1
                        else:
                            self.retry_timer = self.retry_timer*2
                            if self.retry_timer >= self.retry_timer_max:
                                self.retry_timer = self.retry_timer_max
                    
                    #If token expires, login again and get new token
                    if res.status_code == self.expired_code:
                        if encountered_401 == True:
                            self.logger.error('ERROR - Can not perform API operations')
                            self.logger.warning('Steps to troubleshoot: ')
                            self.logger.warning('1) Ensure Access Key has proper permission.')
                            self.logger.warning('2) Ensure Prisma Cloud license is valid.')
                            self.logger.warning('3) If using a CWPP Project, ensure project name is valid in credential configurations.')
                            exit()

                        self.logger.error(f'FAILED {self.expired_code} - {time_completed} seconds')
                        self.logger.warning('Session expired. Generating new Token and retrying')
                        self._api_login_wrapper()
                        encountered_401 = True

                    self.logger.warning(f'Retrying request')
                    self.logger.debug(f'{url}')

                    res, time_completed = self.__request_wrapper(method, url, headers=self.headers, json=json, data=data, params=params, verify=verify, acceptCsv=acceptCsv)
                    retries += 1
                
                if res.status_code in self.success_status or res.status_code in status_ignore:
                    try:
                        self.logger.success(f'SUCCESS - {time_completed} seconds')
                    except:
                        self.logger.info(f'SUCCESS - {time_completed} seconds')
                    return res

                if retries >= self.retries:
                    self.logger.error('ERROR. Max retires exceeded')

                #Some redlock errors need to be handled elsewhere and don't require this debugging output
                if 'x-redlock-status' in res.headers and redlock_ignore:
                    for el in redlock_ignore:
                        if el in res.headers['x-redlock-status']:
                            return res

                code = "NO_CODE"
                try:
                    code = res.status_code
                except:
                    pass
                self.logger.error(f'FAILED {code} - {time_completed} seconds')
                self.logger.error('REQUEST DUMP:')
                self.logger.warning('REQUEST HEADERS:')
                self.logger.info(self.headers)
                self.logger.warning('REQUEST JSON:')
                self.logger.info(json)
                if data:
                    self.logger.warning('REQUEST DATA:')
                    self.logger.info(data)
                self.logger.warning('REQUEST PARAMS:')
                self.logger.info(params)
                self.logger.warning('RESPONSE:')
                self.logger.info(res)
                self.logger.warning('RESPONSE URL:')
                self.logger.info(res.url)
                self.logger.warning('RESPONSE HEADERS:')
                self.logger.info(res.headers)
                self.logger.warning('RESPONSE REQUEST BODY:')
                self.logger.info(res.request.body)
                self.logger.warning('RESPONSE STATUS:')
                if 'x-redlock-status' in res.headers:
                    self.logger.info(res.headers['x-redlock-status'])
                self.logger.warning('RESPONSE TEXT:')
                self.logger.info(res.text)
                self.logger.warning('RESPONSE JSON:')
                if res.text != "":
                    for json_data in res.json():
                        self.logger.info(json_data)

                self.u_count = 1
                return res
            except KeyboardInterrupt:
                self.logger.error('Keyboard Interrupt. Exiting...')
                exit()
            except Exception as e:
                #self.logger.error(e, f'- {time_completed} seconds')
                self.logger.error(e)
                if res == self.empty_res:
                    self.logger.error(f'UNKNOWN ERROR - API Call Wrapper. Retrying... {self.u_count} of {self.unknown_error_max}')
                    time.sleep(2)
                else:
                    self.logger.error(f'UNKNOWN ERROR - API Call Wrapper. Continuing... {self.u_count} of {self.unknown_error_max}')
                self.u_count += 1

    #==============================================================================

    def request(self, method: str, endpoint_url: str, json: dict=None, data: dict=None, params: dict=None, verify=None, acceptCsv=False, redlock_ignore: list=None, status_ignore: list=[], custom_log='', custom_error_message=''):
        '''
        Function for calling the PC API using this session manager. Accepts the
        same arguments as 'requests.request' minus the headers argument as 
        headers are supplied by the session manager.
        '''
        if verify == None:
            verify = self.verify

        #If the CWP Session is a project, auto add project id query string
        try:
            if self.project_flag == True:
                if params:
                    params.update({"project":self.tenant})
                else:
                    params = {"project":self.tenant}
        except:
            pass

        #Validate method
        method = method.upper()
        if method not in ['POST', 'PUT', 'GET', 'OPTIONS', 'DELETE', 'PATCH']:
            self.logger.warning('Invalid method.')
        
        #Build url
        if endpoint_url[0] != '/':
            endpoint_url = '/' + endpoint_url

        url = f'{self.api_url}{endpoint_url}'

        #Call wrapper
        return self.__api_call_wrapper(method, url, json=json, data=data, params=params, verify=verify, acceptCsv=acceptCsv, redlock_ignore=redlock_ignore, status_ignore=status_ignore, custom_log=custom_log, custom_error_message=custom_error_message)

    def config_search_request(self, json: dict, verify=None, acceptCsv=False, redlock_ignore: list=None, status_ignore: list=[]):
        if verify == None:
            verify = self.verify
        
        limit = 20000#Max limit value is 100,000
        
        #Force best practices with HS
        json.update({"heuristicSearch": True, "limit": limit, "withResourceJson": True})

        #initial API Call
        res = self.__api_call_wrapper('POST', f'{self.api_url}/search/config', json=json, verify=verify, acceptCsv=acceptCsv, redlock_ignore=redlock_ignore, status_ignore=status_ignore)

        total_rows = 0
        complete_res_list = []
        complete_res_dict = res.json()

        #res_data var used for while loop
        res_data = res.json()['data']

        complete_res_list.extend(res_data.get('items'))

        retrievedRows = res_data.get('totalRows')
        total_rows += retrievedRows

        counter = 0
        while 'nextPageToken' in res_data:
            #update payload
            json.update({'pageToken': res_data.get('nextPageToken')})

            #call page endpoint
            res = self.__api_call_wrapper('POST', f'{self.api_url}/search/config/page', json=json, verify=verify, acceptCsv=acceptCsv, redlock_ignore=redlock_ignore, status_ignore=status_ignore)
            counter += 1

            #update res_data with the paginated response
            res_data = res.json()

            #Add results from each page API call
            complete_res_list.extend(res_data.get('items'))

            retrievedRows = res_data.get('totalRows')
            total_rows+= retrievedRows

        #Update res dict to be the some format as the 'data' object in a typical RQL res
        complete_res_dict['data'].update({'totalRows':total_rows, 'items': complete_res_list})

        return complete_res_dict

    def config_search_request_function(self, json, function, verify=None, acceptCsv=False,  redlock_ignore: list=None, status_ignore: list=[]):
        if verify == None:
            verify = self.verify
        
        limit = 2000#Max limit value is 100,000
        
        #Force best practices with HS
        json.update({"heuristicSearch": True, "limit": limit, "withResourceJson": True})

        #initial API Call
        res = self.__api_call_wrapper('POST', f'{self.api_url}/search/config', json=json, verify=verify, acceptCsv=acceptCsv, redlock_ignore=redlock_ignore, status_ignore=status_ignore)
        
        total_rows = res.json()['data']['totalRows']

        res_details = res.json()
        res_details.pop('data')
        res_data = res.json()['data']
        counter = 0

        function(res_details, res_data, counter, total_rows)

        while 'nextPageToken' in res_data:
            #update payload
            json.update({'pageToken': res_data.get('nextPageToken')})

            #call page endpoint
            res = self.__api_call_wrapper('POST', f'{self.api_url}/search/config/page', json=json, verify=verify, acceptCsv=acceptCsv, redlock_ignore=redlock_ignore, status_ignore=status_ignore)
            counter += 1

            res_data = res.json()
            total_rows += res_data['totalRows']

            function(res_details, res_data, counter, total_rows)

        return total_rows

    def __request_wrapper(self, method, url, headers, json, data, params, verify, acceptCsv):
        if acceptCsv == True: #CSPM Support Only
            headers.update({
                'Accept': 'text/csv'
            })

        r = self.empty_res

        start_time = time.time()
        r = requests.request(method, url, headers=headers, json=json, data=data, params=params, verify=verify)
        end_time = time.time()
        time_completed = round(end_time-start_time,3)

        while r == self.empty_res and self.u_count < self.unknown_error_max:
            try:
                start_time = time.time()
                r = requests.request(method, url, headers=headers, json=json, data=data, params=params, verify=verify)
                end_time = time.time()
                time_completed = round(end_time-start_time,3)

                self.u_count = 1
                return [r, time_completed]
            except KeyboardInterrupt:
                self.logger.error('Keyboard Interrupt. Exiting...')
                exit()
            except Exception as e:
                self.logger.error(e)
                self.logger.error(f'UNKNOWN ERROR - Request Wrapper. Retrying {self.u_count} of {self.unknown_error_max}')
                time.sleep(2)
                self.u_count += 1

        return [r, time_completed]