#Standard Library
import time

#installed
import requests

from urllib3.exceptions import InsecureRequestWarning

class Session:
    def __init__(self,logger):
        """
        Initalizes a Prisma Cloud API Session Manager.

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
        self.token_time = 480

        self.empty_res = ''

        self.unknown_error_max = 5

        self.logger = logger

#==============================================================================
    def _api_login_wrapper(self):
        if self.verify == False:
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

        res = self.empty_res
        u_count = 0
        while res == self.empty_res and u_count < self.unknown_error_max:
            try:
                res = self._api_login()

                retries = 0
                while res.status_code in self.retry_statuses and retries < self.retries:
                    if res.status_code in self.retry_delay_statuses:
                        self.logger.warning('Increaseing wait time.')
                        #Increase timer when ever encounted to slow script execution.
                        if self.retry_timer == 0:
                            self.retry_timer = 1
                        else:
                            self.retry_timer = self.retry_timer*2
                            if self.retry_timer >= self.retry_timer_max:
                                self.retry_timer = self.retry_timer_max

                        time.sleep(self.retry_timer)

                    elif res.status_code == self.expired_code:
                        self._expired_login()
                    else:
                        self.logger.error('FAILED')
                        self.logger.error('ERROR Logging In. JWT not generated.')
                        self.logger.warning('RESPONSE:')
                        self.logger.info(res)
                        self.logger.warning('RESPONSE URL:')
                        self.logger.info(res.url)
                        self.logger.warning('RESPONSE TEXT:')
                        self.logger.info(res.text)
                    
                    res = self._api_login()

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
                    self.logger.success('SUCCESS')
                except:
                    self.logger.info('SUCCESS')

                return token

            except KeyboardInterrupt:
                self.logger.error('Keyboard Interrupt. Exiting...')
                exit()
            except Exception as e:
                self.logger.error(e)
                u_count += 1
                self.logger.error(f'UNKNOWN ERROR - API login. Retrying... {u_count} of {self.unknown_error_max}')
                self.logger.warning('Steps to troubleshoot: ')
                self.logger.warning('1) Disable any VPNs.')
                self.logger.warning('2) Ensure API base URL is correct.')
                time.sleep(1)

    def _api_refresh_wrapper(self):
        res = self.empty_res
        u_count = 0
        while res == self.empty_res and u_count < self.unknown_error_max:
            try:
                res = self._api_refresh()

                retries = 0
                while res.status_code in self.retry_statuses and retries < self.retries:
                    if res.status_code in self.retry_delay_statuses:
                        self.logger.warning('Increasing wait time.')
                        #Increase timer when ever encounter to slow script execution.
                        if self.retry_timer == 0:
                            self.retry_timer = 1
                        else:
                            self.retry_timer = self.retry_timer*2
                            if self.retry_timer >= self.retry_timer_max:
                                self.retry_timer = self.retry_timer_max

                        time.sleep(self.retry_timer)

                    elif res.status_code == self.expired_code:
                        self._expired_login()
                    else:
                        self.logger.error('FAILED')
                        self.logger.error('ERROR Refreshing Token.')
                        self.logger.warning('RESPONSE:')
                        self.logger.info(res)
                        self.logger.warning('RESPONSE URL:')
                        self.logger.info(res.url)
                        self.logger.warning('RESPONSE TEXT:')
                        self.logger.info(res.text)
                    
                    res = self._api_refresh()

                    retries +=1
                
                if retries == self.retries:
                    self.logger.error('ERROR. Max retires exceeded on JWT refresh. Exiting...')
                    exit()

                try:
                    self.logger.success('SUCCESS')
                except:
                    self.logger.info('SUCCESS')

                return

            except KeyboardInterrupt:
                self.logger.error('Keyboard Interrupt. Exiting...')
                exit()
            except Exception as e:
                self.logger.error(e)
                u_count += 1
                self.logger.error(f'UNKNOWN ERROR - API refresh. Retrying... {u_count} of {self.unknown_error_max}')
                self.logger.warning('Steps to troubleshoot: ')
                self.logger.warning('1) Disable any VPNs.')
                self.logger.warning('2) Ensure API base URL is correct.')
                time.sleep(1)


#==============================================================================
    def __api_call_wrapper(self, method: str, url: str, json: dict=None, data: dict=None, params: dict=None, verify=True, acceptCsv=False, redlock_ignore: list=None, status_ignore: list=[]):
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
        u_count = 0
        while res == self.empty_res and u_count < self.unknown_error_max:
            try:
                if time.time() - self.token_time_stamp >= self.token_time:
                    self.logger.warning('Session Refresh Timer - Generating new Token')
                    self._api_refresh_wrapper()

                self.logger.debug(f'{url}')
                res = self.__request_wrapper(method, url, headers=self.headers, json=json, data=data, params=params, verify=verify, acceptCsv=acceptCsv)
                
                if res.status_code in self.success_status or res.status_code in status_ignore:
                    try:
                        self.logger.success('SUCCESS')
                    except:
                        self.logger.info('SUCCESS')
                    return res

                retries = 0
                while res.status_code in self.retry_statuses and retries < self.retries:
                    #If we get a 429 code, sleep for a doubling ammount of time.
                    if res.status_code in self.retry_delay_statuses:
                        #Wait for retry timer
                        if self.retry_timer > 0:
                            time.sleep(self.retry_timer)

                        self.logger.warning('Increaseing wait time.')
                        #Increase timer when ever wait status encounted to slow script execution.
                        if self.retry_timer == 0:
                            self.retry_timer = 1
                        else:
                            self.retry_timer = self.retry_timer*2
                            if self.retry_timer >= self.retry_timer_max:
                                self.retry_timer = self.retry_timer_max
                    
                    #If token expires, login again and get new token
                    if res.status_code == 401:
                        self.logger.warning('Session expired. Generating new Token and retrying.')
                        self._api_login_wrapper()

                    self.logger.warning(f'Retrying request. Code {res.status_code}.')
                    self.logger.debug(f'{url}')

                    res = self.__request_wrapper(method, url, headers=self.headers, json=json, data=data, params=params, verify=verify, acceptCsv=acceptCsv)
                    retries += 1
                
                if res.status_code in self.success_status or res.status_code in status_ignore:
                    try:
                        self.logger.success('SUCCESS')
                    except:
                        self.logger.info('SUCCESS')
                    return res

                if retries >= self.retries:
                    self.logger.error('ERROR. Max retires exceeded')

                #Some redlock errors need to be handled elsewhere and don't require this debugging output
                if 'x-redlock-status' in res.headers and redlock_ignore:
                    for el in redlock_ignore:
                        if el in res.headers['x-redlock-status']:
                            return res

                self.logger.error('FAILED')
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

                return res
            except KeyboardInterrupt:
                self.logger.error('Keyboard Interrupt. Exiting...')
                exit()
            except Exception as e:
                self.logger.error(e)
                u_count += 1
                if res == self.empty_res:
                    self.logger.error(f'UNKNOWN ERROR - API Call Wrapper. Retrying... {u_count} of {self.unknown_error_max}')
                    time.sleep(1)
                else:
                    self.logger.error(f'UNKNOWN ERROR - API Call Wrapper. Continuing... {u_count} of {self.unknown_error_max}')

    #==============================================================================

    def request(self, method: str, endpoint_url: str, json: dict=None, data: dict=None, params: dict=None, verify=True, acceptCsv=False, redlock_ignore: list=None, status_ignore: list=[]):
        '''
        Function for calling the PC API using this session manager. Accepts the
        same arguments as 'requests.request' minus the headers argument as 
        headers are supplied by the session manager.
        '''
        #Validate method
        method = method.upper()
        if method not in ['POST', 'PUT', 'GET', 'OPTIONS', 'DELETE', 'PATCH']:
            self.logger.warning('Invalid method.')
        
        #Build url
        if endpoint_url[0] != '/':
            endpoint_url = '/' + endpoint_url

        url = f'{self.api_url}{endpoint_url}'

        #Call wrapper
        return self.__api_call_wrapper(method, url, json=json, data=data, params=params, verify=verify, acceptCsv=acceptCsv, redlock_ignore=redlock_ignore, status_ignore=status_ignore)


    def __request_wrapper(self, method, url, headers, json, data, params, verify, acceptCsv):
        if acceptCsv == True: #CSPM Support Only
            headers.update({
                'Accept': 'text/csv'
            })

        u_count = 0
        r = self.empty_res
        while r == self.empty_res and u_count < self.retries:
            u_count += 1
            try:
                r = requests.request(method, url, headers=headers, json=json, data=data, params=params, verify=verify)
                return r
            except KeyboardInterrupt:
                self.logger.error('Keyboard Interrupt. Exiting...')
                exit()
            except Exception as e:
                self.logger.error(e)
                u_count += 1
                self.logger.error(f'UNKNOWN ERROR - Request Wrapper. Retrying {u_count} of {self.unknown_error_max}')
                time.sleep(1)

            

        return requests.request(method, url, headers=headers, json=json, data=data, params=params)