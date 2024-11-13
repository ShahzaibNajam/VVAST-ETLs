import requests #not standard
import json
from ratelimit import limits, sleep_and_retry

class APIRequests:

    def __init__ (self, logger, app_reference, account_token):

        self.log = logger

        self.app_reference = app_reference

        self.account_token = account_token

        self.api_timeoff = 20 #Amount of time to wait when request timeout is reached

    One_MINUTE = 60 
    @sleep_and_retry
    @limits(calls=60, period=One_MINUTE)
    def do_request(self, type_of_request, uri_to_pass, params=""):

        try:

            response = ""

            if type_of_request == "get":

                response = requests.get(uri_to_pass
                                        ,headers={"brightpearl-app-ref": self.app_reference
                                        ,"brightpearl-account-token": self.account_token}
                                        ,params=params
                )

            elif type_of_request == "options":

                response = requests.options(uri_to_pass
                                        ,headers={"brightpearl-app-ref": self.app_reference
                                        ,"brightpearl-account-token": self.account_token}
                )

            else:

                self.log.error("Wrong request type. Please review")

                return ""
            
            
            if response.status_code == 404 or response.status_code == 400:

                return response.json()
                
            elif response.status_code == 207 or 200:

                return response.json()
                        
            else:

                self.log.error(response.text)                    
        
        except Exception as e:

            self.log.error (e)