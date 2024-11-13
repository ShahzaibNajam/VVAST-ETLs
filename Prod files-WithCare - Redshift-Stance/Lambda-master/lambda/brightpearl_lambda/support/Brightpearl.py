import json
import logging
from enum import Enum
from datetime import datetime,timedelta
import time
from .DBInteraction import PostgresInteraction
from .APIInteraction import APIRequests

"""
Enum object for future extensions - Define a module and its api params
The "is_simple" param was added in the product extension review since some modules 
don't use the OPTIONS request type. 
If it's true :
    - It won't run the OPTIONS request.

The "is_bridge_table" param was added the product extension review since some modules
have the OPTIONS request but the SEARCH capability is severely limited. Using OPTIONS you
can parse the IDs from the URIs that are retrieved. This seems to be common in bridge tables.
If it's true :
    - It will run OPTIONS requests but won't perform SEARCH at all.
"""
class BrightpearlModule(Enum):
    
    #This first one will have the explanation of what these enums are for
    PRODUCT = {"Id":"productId" #Brightpearl ID
               ,"databaseId":"dbproductidoptionvalue" #Database primary key. Might coincide with Brightpearl ID.
               ,"search_reference":"/product-service/product-search" #the uri to do a search on Brightpearl API if available
               ,"single_reference":"/product-service/product" #The uri to get an entity 
               ,"set_retrieval":"/product-service" # get all the entities
               ,"table_name": "products" # the name of the table in the DB
               ,"is_simple" : False # If the module doesn't allow the OPTIONS request
               ,"is_bridge_table" : False # IF the module doesn't allow SEARCH.
               ,"post_filter": "" # which entity should we look up for ids in case not the one we are processing. For example product availability. 
                                  # We want to use product ids. 
               ,"has_hard_deletes": False # If the module does hard deletes on pks instead of updates.
                }

    ORDER = {"Id":"orderId"
               ,"databaseId":"orderId"    
               ,"search_reference":"/order-service/order-search"
               ,"single_reference":"/order-service/order"
               ,"set_retrieval":"/order-service"
               ,"table_name": "orders"
               ,"is_simple" : False
               ,"is_bridge_table" : False
                ,"post_filter": ""
               ,"has_hard_deletes": False
                }

    ORDERITEM = {"Id":"orderId"
               ,"databaseId":"fkorderid"    
               ,"search_reference":"/order-service/order-search"
               ,"single_reference":"/order-service/order"
               ,"set_retrieval":"/order-service"
               ,"table_name": "orderitems"
               ,"is_simple" : False
               ,"is_bridge_table" : False
                ,"post_filter": ""
               ,"has_hard_deletes": False
                }                
    
    PRODUCTOPTIONVALUE = {"Id":"optionValueId"
               ,"databaseId":"optionValueId"
               ,"search_reference":"/product-service/option-value-search"
               ,"single_reference":"/product-service/option/{id-set}/value"
               ,"set_retrieval":"/product-service/option"
               ,"table_name": "productsoptionvalue"
               ,"is_simple" : True
               ,"is_bridge_table" : False
               ,"post_filter": ""
               ,"has_hard_deletes": False
                }
    PRODUCTTYPE = {"Id":"id"
               ,"databaseId":"productTypeId"
               ,"search_reference":"/product-service/product-type-search"
               ,"single_reference":"/product-service/product-type/{id-set}"
               ,"set_retrieval":"/product-service/type"
               ,"table_name": "producttype"
               ,"is_simple" : True
               ,"is_bridge_table" : False
               ,"post_filter": ""
               ,"has_hard_deletes": False
               ,"is_search":True
                }
    PRICELIST = {"Id":"id"
               ,"databaseId":"priceListId"
               ,"search_reference":"/product-service/price-list/"
               ,"single_reference":"/product-service/price-list/{id-set}"
               ,"set_retrieval":"/product-service/type"
               ,"table_name": "pricelist"
               ,"is_simple" : True
               ,"is_bridge_table" : False
               ,"post_filter": ""
               ,"has_hard_deletes": False
               ,"is_search":True
                }
    BRAND = {"Id":"brandId"
               ,"databaseId":"brandId"
               ,"search_reference":"/product-service/brand-search"
               ,"single_reference":"/product-service/brand/{id-set}"
               ,"set_retrieval":"/product-service/brand"
               ,"table_name": "brand"
               ,"is_simple" : True
               ,"is_bridge_table" : False
               ,"post_filter": ""
               ,"has_hard_deletes": False
               ,"is_search":True
                }
    BRIGHTPEARLCATEGORY = {"Id":"id"
               ,"databaseId":"brightpearlCategoryId"
               ,"search_reference":"/product-service/brightpearl-category-search"
               ,"single_reference":"/product-service/brightpearl-category/{id-set}"
               ,"set_retrieval":"/product-service/bpcat"
               ,"table_name": "brightpearlcategory"
               ,"is_simple" : True
               ,"is_bridge_table" : False
               ,"post_filter": ""
               ,"has_hard_deletes": False
               ,"is_search":True
                }
    SEASON = {"Id":"id"
               ,"databaseId":"seasonId"
               ,"search_reference":"/product-service/season/"
               ,"single_reference":"/product-service/season/{id-set}"
               ,"set_retrieval":"/product-service/season"
               ,"table_name": "season"
               ,"is_simple" : True
               ,"is_bridge_table" : False
               ,"post_filter": ""
               ,"has_hard_deletes": False
               ,"is_search":True
                }                
    PRODUCTPRICE = {"Id":"id"
               ,"databaseId":"dbproductpricevalue"
               ,"search_reference":"/product-service/product-price/"
               ,"single_reference":"/product-service/product-price/{id-set}"
               ,"set_retrieval":"/product-service"
               ,"table_name": "productprice"
               ,"is_simple" : True
               ,"is_bridge_table" : False
               ,"post_filter": {"table_reference": "products", "id_reference" : "productid"}
               ,"has_hard_deletes": False
               ,"is_search":True
                }
    PRODUCTAVAILABILITY = {"Id":"Id"
               ,"databaseId":"productavailabilityid"
               ,"search_reference":"/warehouse-service/product-availability"
               ,"single_reference":"/warehouse-service/product-availability/{id-set}"
               ,"set_retrieval":"/warehouse-service/product-availability"
               ,"table_name": "productavailability"
               ,"is_simple" : True
               ,"is_bridge_table" : True
               ,"post_filter": {"table_reference": "products", "id_reference" : "productid"}
               ,"has_hard_deletes": False
               ,"is_search":True
                }

    FULFILMENTSTATUS = {"Id":"Id"
               ,"databaseId":"productavailabilityid"
               ,"search_reference":"/warehouse-service/product-availability"
               ,"single_reference":"/warehouse-service/product-availability/{id-set}"
               ,"set_retrieval":"/warehouse-service/product-availability"
               ,"table_name": "productavailability"
               ,"is_simple" : True
               ,"is_bridge_table" : True
               ,"post_filter": {"table_reference": "orders", "id_reference" : "orderid"}
               ,"has_hard_deletes": False
                }
    
    CONTACT = {"Id":"contactId"
               ,"databaseId":"contactId"    
               ,"search_reference":"/contact-service/contact-search"
               ,"single_reference":"/contact-service/contact"
               ,"set_retrieval":"/contact-service"
               ,"table_name": "contacts"
               ,"is_simple" : False
               ,"is_bridge_table" : False
                ,"post_filter": ""
                ,"has_hard_deletes": False 
                             
                }
    GoodsInventory={"Id":"goodsMovementId"
               ,"databaseId":"goodsmovementid"    
               ,"search_reference":"/warehouse-service/goods-movement-search"
               ,"single_reference":"/warehouse-service/goods-movement-search?goodsMovementId={id-set}"
               ,"set_retrieval":"/warehouse-service/goods-in-search"
               ,"table_name": "goodsinventory"
               ,"is_simple" : True
               ,"is_bridge_table" : False
                ,"post_filter": ""
                ,"has_hard_deletes": False 
                ,"is_search":True                
                }
    COMPANY = {"Id":"companyId"
               ,"databaseId":"companyid"    
               ,"search_reference":"/contact-service/company-search"
               ,"single_reference":"/contact-service/company/{id-set}"
               ,"set_retrieval":"/contact-service"
               ,"table_name": "company"
               ,"is_simple" : True
               ,"is_bridge_table" : False
                ,"post_filter": ""
                ,"has_hard_deletes": False
                ,"is_search":True               
                }
    TAGS = {"Id":"tagId"
               ,"databaseId":"tagid"    
               ,"search_reference":"/contact-service/tag"
               ,"single_reference":"/contact-service/tag/{id-set}"
               ,"set_retrieval":"/contact-service"
               ,"table_name": "contacttags"
               ,"is_simple" : True
               ,"is_bridge_table" : False
               ,"post_filter": ""
               ,"has_hard_deletes": False
               ,"is_search":False
                }
    CUSTOMERPAYMENT = {"Id":"paymentId"
               ,"databaseId":"paymentId"    
               ,"search_reference":"/accounting-service/customer-payment-search"
               ,"single_reference":"/accounting-service/customer-payment-search?paymentId={id-set}"
               ,"set_retrieval":"/accounting-service"
               ,"table_name": "customerpayment"
               ,"is_simple" : True
               ,"is_bridge_table" : False
               ,"post_filter": ""
               ,"has_hard_deletes": False
               ,"is_search":False
                }
    CHANNEL = {"Id":"id"
               ,"databaseId":"Id"
               ,"search_reference":"/product-service/channel/"
               ,"single_reference":"/product-service/channel/{id-set}"
               ,"set_retrieval":"/product-service/channel/"
               ,"table_name": "channel"
               ,"is_simple" : True
               ,"is_bridge_table" : False
               ,"post_filter": {}
               ,"has_hard_deletes": False
               ,"is_search":True
                }
               
    WAREHOUSE = {"Id":"id"
               ,"databaseId":"Id"
               ,"search_reference":"/warehouse-service/warehouse/"
               ,"single_reference":"/warehouse-service/warehouse/{id-set}"
               ,"set_retrieval":"/warehouse-service/warehouse/"
               ,"table_name": "warehouse"
               ,"is_simple" : True
               ,"is_bridge_table" : False
               ,"post_filter": {}
               ,"has_hard_deletes": False
               ,"is_search":True
                }
               
class BrightpearlAPIInteraction:
    
    def __init__ (self, logger, app_reference, account_name, account_token, schema_to_handle):
                
        self.base_uri = "https://ws-eu1.brightpearl.com/public-api/"
        
        self.account_name = account_name
                
        self.log = logger

        self.schema_to_handle = schema_to_handle  

        self.api = APIRequests(logger, app_reference, account_token) # Branched out api requests object easier to test and recover after a fail

    #get all the IDs from the Brightpearl account - dependent on the module being passed    
    def get_ids_from_entity(self, module_segment, timestamp, database_service=None):
        
        list_of_ids_from_entity = []
        
        module_info = module_segment.value
        tablename=module_info["table_name"]
        
        call_url = self.base_uri + self.account_name + module_info["search_reference"]

        #self.log.debug(call_url)

        #For further explanation on this behavior please refer to the Enum object comments above.
        if module_info["is_bridge_table"] == False:                                
            
            """
            pagination variables - Brightpearl paginates the search requests by using a first result logic:
            it paginates per 500 results and then you request which page of this result set you want. 
            """
            more_results = True
            current_result = 1
            now = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H:%M:%S")
            #Timedelt=(datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")+timedelta(days=7))
            #Timedelt2=datetime.strftime(Timedelt,"%Y-%m-%dT%H:%M:%S")
            self.log.info("Connecting to the API...")
            #start_Date='2020-01-10T00:00:01'
            #while start_Date<'2020-01-24T00:00:01'
            while more_results == True:
                if tablename=="customerpayment":    
                                                print("In CP")
                                                parameters = {"columns":module_info["Id"]# remaain  remain,2018
                                                                            ,"createdOn": timestamp + "/" + now#>yeti max inventory date '2019-12-31T23:59:59'
                                                                            ,"firstResult": current_result}
                elif tablename=="channel" or tablename=="warehouse":
                    print("Not in CP")
                    parameters = {"columns":module_info["Id"]
                                                ,"updatedOn": '1970-01-01T00:00:01' + "/" +now#>yeti max inventory date
                                                ,"firstResult": current_result}
                else:
                    print("Not in CP")
                    parameters = {"columns":module_info["Id"]
                                                ,"updatedOn": timestamp + "/" +now#>yeti max inventory date
                                                ,"firstResult": current_result}
                
                #print(parameters)
                #'2021-05-31T00:00:01'
                response_as_json = self.api.do_request("get", call_url, parameters)
                #print(response_as_json)            
                """
                Some modules don't have SEARCH functionality. For those the json parsing
                would fail since the required field is not available.
                For the flow to remain intact we must create a case for this modules.
                """

                #test for API throtling
                if "response" in response_as_json:

                    while response_as_json["response"] == "You have sent too many requests. Please wait before sending another request":

                        self.log.info("API request limit reached. Waiting " + str(self.api.api_timeoff) + "s")
                        time.sleep(self.api.api_timeoff)

                        self.log.info("Firing request again to: "+ call_url)
                        response_as_json = self.api.do_request("get", call_url, parameters)
                        #self.log.info(response_as_json)

                if "errors" in response_as_json:

                    context = {"loginname":database_service.db_schema
                                ,"modulename": module_info["table_name"]
                                ,"errordescription":response_as_json["errors"][0]["message"]}

                    database_service.insert_error_in_table(context)

                    self.log.error(response_as_json["errors"][0]["message"])

                    more_results = False

                elif "results" not in response_as_json["response"]:
                    if tablename=="contacttags":

                        self.log.info("Connected to API. Receiving page " + str(current_result))

                        for element in list(response_as_json["response"]):
                            list_of_ids_from_entity.append(int(element))

                        more_results=False;
                    
                    else:
                        self.log.info("Search module not available for this entity. Parsing unique ids...")
                        #print(response_as_json["response"])
                        #parse the id list from the ids of the response
                        for ids in response_as_json["response"]:
                        
                            #This has to be converted to a list because that's what the return is: a list of lists
                            list_of_ids_from_entity.append([ids[module_info["Id"]]])
                        
                            #for modules without SEARCH the parsing ends here.

                        more_results = False

                else:
                    
                    
                    self.log.info("Connected to API. Receiving page " + str(current_result))

                    for element in list(response_as_json["response"]["results"]):
                        
                        list_of_ids_from_entity.append(element)

                    if response_as_json["response"]["metaData"]["morePagesAvailable"] == True:
                                
                        last_result = response_as_json["response"]["metaData"]["lastResult"]
                        
                    # This way the request will get the next result set
                        current_result = last_result + 1
                    
                    else:
                        
                    #Stop iterating and return list
                    
                        more_results = False
        else:

            """

            uris_from_bridge_table = self._options_request(call_url)

            #Looks a bit weird but saves some extra requests and a duplicate logic - parses the ids from the URIs
            for uri in uris_from_bridge_table["response"]["getUris"]:
                
                uri_separator = uri.rfind("/")
                max_len = len(uri)

                uri = uri[uri_separator + 1:max_len]
                uri = uri.replace(",","-")

                for final_uri in uri.split("-"):

                    list_of_ids_from_entity.append([int(final_uri)])
            """
            self.log.info("This is a bridge table. Won't retrieve any ids")                    

        
        return list_of_ids_from_entity
    
    def _chunk_ids_into_requests(self, entity_list, module_info, number_of_ids_in_chunk=59):

        try:

            work_list_for_ids = []

            if len(entity_list) == 1:

                work_list_for_ids.append(str(min(entity_list)[0]))

            elif len(entity_list) == 0:

                return work_list_for_ids
            
            elif len(entity_list) <= number_of_ids_in_chunk and module_info["is_simple"] == True:
            
                if module_info["table_name"]=="contacttags":
                    entity_list.sort()  
                    for e in entity_list:
                        work_list_for_ids.append(str(e))  
                else:
                    entity_list.sort()
                    work_list_for_ids.append(",".join(str(e[0]) for e in entity_list))

            else:            

                
                if module_info["is_simple"] == False:
                    list_of_ids = [entity_list[i:i + number_of_ids_in_chunk] for i in range(0, len(entity_list), number_of_ids_in_chunk)]
                    
                    for l in list_of_ids:
                        
                        work_list_for_ids.append(",".join(str(e[0]) for e in l))

                else:
                    
                    processing_list = [u[0] for u in entity_list]
                    processing_list.sort()
                    sequential_item_list = []

                    for i in range(0, len(processing_list)):

                        try:

                            if abs(processing_list[i+1] - processing_list[i]) == 1 and len(sequential_item_list) < 199:

                                sequential_item_list.append(processing_list[i])

                            else:

                                if len(sequential_item_list) == 0:

                                    work_list_for_ids.append(str(processing_list[i]))
                                
                                else:

                                    sequential_item_list.append(processing_list[i])

                                    work_list_for_ids.append(str(min(sequential_item_list)) + "-" 
                                    + str(max(sequential_item_list)))

                                    sequential_item_list = []
                                                            
                        except IndexError:
                            print("In index")
                            if len(sequential_item_list)>0:
                                
                                work_list_for_ids.append(str(min(sequential_item_list)) + "-" 
                                        + str(max(sequential_item_list)))

                            work_list_for_ids.append(str(processing_list[i]))

                            sequential_item_list = []

            return work_list_for_ids

        except Exception as i:
            
            self.log.error(i)

    #get module Id details to parse later - depends on the module being passed, id must be a list
    def get_details_from_entity (self, module_segment, entity_list, database_service=None):
        
        """
        In order to retrieve large datasets we need to take advantage of Brightpearl
        API options. We pass a set of IDs and the API returns some urls to get the 
        data from.
        """
        module_info = module_segment.value
        
        #parse for the uri except if it only contains one or no element. Otherwise causes failures in the call
        
        work_list_for_ids = self._chunk_ids_into_requests(entity_list, module_info) # this list will be used to optimize the requests.
        #print("Work_list_if_ids",work_list_for_ids)
        list_of_entities_to_return = []
        is_simple = module_info["is_simple"]
        
        # After we organized all the required ids in lists we make the requests.
        try:


            for string_of_ids in work_list_for_ids:
                    
                if is_simple == False:


                    call_url = self.base_uri + self.account_name + module_info["single_reference"] + "/" + string_of_ids
                    self.log.debug(call_url)

                    #get uris as json
                    
                    uri_to_process = self.api.do_request("options", call_url)
                    while uri_to_process["response"] == "You have sent too many requests. Please wait before sending another request":

                            self.log.info("API request limit reached. Waiting " + str(self.api.api_timeoff) + "s")
                            time.sleep(self.api.api_timeoff)
                            

                            self.log.info("Firing request again to: "+ call_url)
                            uri_to_process = self.api.do_request("options", call_url)
                            
                      
                    for uri in uri_to_process["response"]["getUris"]:
                        
                        #self.log.info("Getting data from: " + str(uri))

                        uri_call = self.base_uri + self.account_name + module_info["set_retrieval"] + str(uri)

                        result = self.api.do_request("get",uri_call)
                        
                        while result["response"] == "You have sent too many requests. Please wait before sending another request":

                            self.log.info("API request limit reached. Waiting " + str(self.api.api_timeoff) + "s")
                            time.sleep(self.api.api_timeoff)

                            self.log.info("Firing request again to: "+ uri_call)
                            result = self.api.do_request("get",uri_call)
                            #self.log.info(result)

                        #parse the results from the json and store them in a list
                        for entities in result["response"]:                
                            
                            list_of_entities_to_return.append(entities)

                elif is_simple == True:
                    
                    if len(string_of_ids) > 0:
                        
                        self.log.info("Getting details for ids: " + str(string_of_ids))

                        call_url = self.base_uri + self.account_name + module_info["single_reference"].replace("{id-set}",string_of_ids)

                        self.log.debug(call_url)            

                        result = self.api.do_request("get",call_url)

                        #parse the results from the json and store them in a list

                        if "errors" in result:

                            context = {"loginname":database_service.db_schema
                                    ,"modulename": module_info["table_name"]
                                    ,"errordescription":result["errors"][0]["message"]}

                            database_service.insert_error_in_table(context)

                            self.log.error(result["errors"][0]["message"])

                            next

                        elif type(result["response"]) is dict:
                            print("In dict")
                            #print(result["response"])
                            list_of_entities_to_return.append(result["response"])

                        else:

                            if len(result["response"]) > 0:

                                while result["response"] == "You have sent too many requests. Please wait before sending another request":

                                    self.log.info("API request limit reached. Waiting " + str(self.api.api_timeoff) + "s")
                                    time.sleep(self.api.api_timeoff)
                                    print("Firing request again to: "+ call_url)
                                    result = self.api.do_request("get",call_url)
                                    #self.log.info(result)                                

                                for entities in result["response"]:
                                
                                    list_of_entities_to_return.append(entities)
                            
                            else:
                                self.log.info("Although well formed, nothing was returned from the request")

                    else:
                        
                        self.log.info("No ids to request to request")
                
                else:
                    
                    raise Exception ("is_simple parameter must be defined in the enum")
            
        except TypeError as te:

            self.log.error(te + " :" + string_of_ids + result)

            next

        finally:

            return list_of_entities_to_return

class BrightpearlIntegrationInteraction:

    def __init__(self, log, entity, brightpearl_api_interface, db_context):

        self.entity = entity

        self.log = log

        self.entity_name = str(entity.name)

        self.brightpearl_api_interface = brightpearl_api_interface

        self.db_context = db_context
        
       

    def __get_ids_to_delete (self, ids_from_brightpearl, ids_from_db):
        
        # ids_from_db should be a list and ids_from_brightpearl should be a list of lists.
        set_from_bp = set()
        set_from_db = set()
        ids_to_delete = set()

        if len(ids_from_brightpearl) > 0:

            for pk in ids_from_brightpearl:

                set_from_bp.add(pk[0])

            for pk in ids_from_db:

                set_from_db.add(pk[0])

            ids_to_delete = set_from_db - set_from_bp

        return ids_to_delete
        

    def persist_modules_with_reference (self):

        """
        This method will be used to process modules that don't have timestamp incremental
        but use Ids from other tables to update the data. This method has to run at the end of persisting module so it 
        always gets the more recent data
        """

        self.log.info("Started to persist late entity: " + self.entity_name)

        if self.entity.value["post_filter"] != "":
                
            #get late table timestamp
            db1 = PostgresInteraction(self.log, self.db_context
                ,self.brightpearl_api_interface.schema_to_handle, self.entity)
            
            timestamp_to_load = datetime(1970,1,1,0,0,0)

            self.log.info("Process from: " + str(timestamp_to_load))

            #get ids
            
            ids_to_proc = db1.get_ids_on_timestamp(timestamp_to_load)
            #ids_to_proc = self.brightpearl_api_interface.get_ids_from_entity(self.entity, timestamp_to_load, db1)

            self.log.info("Getting details for " + str(len(ids_to_proc)) + " ids")

            list_with_details = self.brightpearl_api_interface.get_details_from_entity(self.entity, ids_to_proc, db1)

            self.log.info("Started persisting to the DB: " + self.entity_name)
                
            """
            insert products in the DB - This is done by calling the method that does the mapping of the detailed
            response with the DB columns. This mapping has to be done manually.
            """

            db1.insert_date_in_bulk(self.__mapping_dbparams_to_response(list_with_details))
                        

        else:
            
            self.log.error("Entity "+self.entity_name+" has no late process info. Nothing will be persisted.")

    def persist_module_segment (self):
            
        #Get all IDs from Brightpearl as a list based on the last insertion
        self.log.info("Started: "+ self.entity_name +" values for " + self.brightpearl_api_interface.schema_to_handle)
        
        #timestamp has to be in the Brightpearl format 
        db1 = PostgresInteraction(self.log, self.db_context
            ,self.brightpearl_api_interface.schema_to_handle, self.entity)
            
        timestamp_to_load = db1.get_timestamp_from_table()
        
        timestamp_to_load = timestamp_to_load.strftime("%Y-%m-%dT%H:%M:%S")
        
        self.log.info("Getting "+self.entity_name+" values from: " + str(timestamp_to_load))
        
        list_of_ids = self.brightpearl_api_interface.get_ids_from_entity(self.entity, timestamp_to_load, db1)
        #import pandas
        #df = pandas.DataFrame(data={"col1": list_of_ids})
        #df.to_csv("./file.csv", sep=',',index=False)
        #import pandas
        #df = pandas.DataFrame(data={"col1": list_of_ids})
        #df.to_csv("./file.csv", sep=',',index=False)
        self.log.info(str(len(list_of_ids)) + " ids retrieved.")
                    
        self.log.info("Started parsing "+self.entity_name+" details...")
        
        #Brightpearl returns a list with a list of IDs - we have to iterate through the Ids
        #with each Id available we get the details for each entity obtained previously
        list_with_details = self.brightpearl_api_interface.get_details_from_entity(self.entity, list_of_ids)     
        
        self.log.info("Finished parsing " + self.entity_name)
        
        #instantiate database object with the required credentials    
        self.log.info("Started persisting to the DB: " + self.entity_name)
        
        """
        insert products in the DB - This is done by calling the method that does the mapping of the detailed
        response with the DB columns. This mapping has to be done manually.
        """
        
        if self.entity.value["has_hard_deletes"] == False:
            #print(self.__mapping_dbparams_to_response(list_with_details))
            db1.insert_data_into_db(self.__mapping_dbparams_to_response(list_with_details))

        else:

            db1.insert_data_into_db_with_deletes(self.__mapping_dbparams_to_response(list_with_details))

        self.log.info("Finished persisting " + self.entity_name)
    
    def persist_module_segment_truncation (self):
 
        """
        This method will be used to process modules that don't have timestamp incremental
        but use Ids from other tables to update the data. This method has to run at the end of persisting module so it 
        always gets the more recent data
        """

        self.log.info("Started to persist late entity: " + self.entity_name)

        if self.entity.value["post_filter"] != "":
                
            #get late table timestamp
            db1 = PostgresInteraction(self.log, self.db_context
                ,self.brightpearl_api_interface.schema_to_handle, self.entity)
            
            timestamp_to_load = datetime(1970,1,1,0,0,0)

            self.log.info("Process from: " + str(timestamp_to_load))

            #get ids
            #ids_to_proc = db1.get_ids_on_timestamp(timestamp_to_load)
            ids_to_proc = self.brightpearl_api_interface.get_ids_from_entity(self.entity, timestamp_to_load, db1)

            self.log.info("Getting details for " + str(len(ids_to_proc)) + " ids")

            list_with_details = self.brightpearl_api_interface.get_details_from_entity(self.entity, ids_to_proc, db1)

            self.log.info("Started persisting to the DB: " + self.entity_name)
                
            """
            insert products in the DB - This is done by calling the method that does the mapping of the detailed
            response with the DB columns. This mapping has to be done manually.
            """

            db1.insert_date_in_bulk(self.__mapping_dbparams_to_response(list_with_details))
                        

        else:
            
            self.log.error("Entity "+self.entity_name+" has no late process info. Nothing will be persisted.")

    def run_truncate_tbl(self):
        db1 = PostgresInteraction(self.log, self.db_context
            ,self.brightpearl_api_interface.schema_to_handle, self.entity)
        db1.truncate_tbl();
        self.log.info("truncate table success");
    
    def run_gi_procs (self):
        
        db1 = PostgresInteraction(self.log, self.db_context
            ,self.brightpearl_api_interface.schema_to_handle, self.entity)
        db1.gi_procs (self.brightpearl_api_interface.schema_to_handle)
        self.log.info("Inventory proc success");

    def __mapping_dbparams_to_response (self, list_with_details):

            """
            params for the insert query - parses the json response and is a value to the parameter key
            Each entity has its own mapping.
            IMPORTANT NOTE: The key of this dictionary will be the column name in the database
            They must be in LOWERCASE. The API parse names must be in camel case.
            """

            entities_to_insert = []

            if self.entity is BrightpearlModule.PRODUCTOPTIONVALUE:
                
                for option_value in list_with_details:

                    entities_to_insert.append({
                                "optionvalueid" : option_value["optionValueId"]
                                ,"optionvaluename": option_value["optionValueName"]
                                ,"optionid" : option_value["optionId"]
                                ,"createdon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                                ,"updatedon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                        })

            if self.entity is BrightpearlModule.PRODUCTAVAILABILITY:

                for availability in list_with_details:

                    try:

                        for product in availability:

                            #for total: warehouse = 0
                            entities_to_insert.append({
                                            "productavailabilityid" : str(product) + "W0"
                                            ,"productid" : product
                                            ,"instock": availability[product]["total"]["inStock"]
                                            ,"onhand": availability[product]["total"]["onHand"]
                                            ,"allocated": availability[product]["total"]["allocated"]
                                            ,"intransit": availability[product]["total"]["inTransit"]
                                            ,"warehouse": 0
                                            ,"createdon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                                            ,"updatedon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                                    })

                            for warehouse in availability[product]["warehouses"]:
                            
                                entities_to_insert.append({
                                            "productavailabilityid" : str(product) + "W" + str(warehouse)
                                            ,"productid" : product
                                            ,"instock": availability[product]["warehouses"][warehouse]["inStock"]
                                            ,"onhand": availability[product]["warehouses"][warehouse]["onHand"]
                                            ,"allocated": availability[product]["warehouses"][warehouse]["allocated"]
                                            ,"intransit": availability[product]["warehouses"][warehouse]["inTransit"]
                                            ,"warehouse": warehouse
                                            ,"createdon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                                            ,"updatedon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                                    })
                    
                    except TypeError:

                        self.log.info(availability)
                        next

            elif self.entity is BrightpearlModule.CHANNEL:

                for channel in list_with_details:

                    entities_to_insert.append({
                                "id" : channel["id"]
                                ,"name": channel["name"]
                                ,"channeltypeid" : channel["channelTypeId"] if "channelTypeId" in channel else 0
                                ,"defaultwarehouseid" : channel["defaultWarehouseId"] if "defaultWarehouseId" in channel else 0
                                ,"contactgroupid" : channel["contactGroupId"] if "contactGroupId" in channel else 0
                                ,"defaultpricelistid" : channel["defaultPriceListId"] if "defaultPriceListId" in channel else 0
                                ,"channelbrandid" : channel["channelBrandId"] if "channelBrandId" in channel else 0
                                ,"createdon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                                ,"updatedon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                        }) 
            
            elif self.entity is BrightpearlModule.WAREHOUSE:

                for warehouse in list_with_details:

                    entities_to_insert.append({
                                "warehouseid" : warehouse["id"]
                                ,"warehousename": warehouse["name"]
                                ,"typecode" : warehouse["typeCode"] if "typeCode" in warehouse else "NA"
                                ,"typedescription" : warehouse["typeDescription"] if "typeDescription" in warehouse else "NA"
                                ,"addressid" : warehouse["address"]["addressId"] if "addressId" in warehouse["address"] else 0
                                ,"customerid" : warehouse["address"]["customerId"] if "customerId" in warehouse["address"] else 0
                                ,"streetaddress" : warehouse["address"]["streetAddress"] if "streetAddress" in warehouse["address"] else "NA"
                                ,"countryid" : warehouse["address"]["countryId"] if "countryId" in warehouse["address"] else 0
                                ,"countryisocode2" : warehouse["address"]["countryIsoCode2"] if "countryIsoCode2" in warehouse["address"] else "NA"
                                ,"createdon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                                ,"updatedon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                        }) 
            
            elif self.entity is BrightpearlModule.GoodsInventory:

                for goods in list_with_details:
                    
                    if len(goods)< 4:
                        for results in goods["results"]:
                                #print(results);
                                entities_to_insert.append({
                                "goodsmovementid" : results[0]
                               ,"productid":results[1]
                               ,"quantity":results[4]
                               ,"warehouseid":results[6]
                               ,"goodsnoteid":results[7]
                               ,"orderid":results[10]
                               ,"goodsnotetypecode":results[14]
                               ,"updatedon":results[15]
                                })
                                
            elif self.entity is BrightpearlModule.PRODUCTTYPE:

                for product_type in list_with_details:

                    entities_to_insert.append({
                                "producttypeid" : product_type["id"]
                                ,"producttypename": product_type["name"]
                                ,"createdon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                                ,"updatedon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                        })
            
            elif self.entity is BrightpearlModule.BRAND:

                for brand in list_with_details:

                    entities_to_insert.append({
                                "brandid" : brand["id"]
                                ,"brandname": brand["name"]
                                ,"branddescription" : brand["description"]
                                ,"createdon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                                ,"updatedon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                        })                            
            
            elif self.entity is BrightpearlModule.PRICELIST:

                for price_list in list_with_details:

                    entities_to_insert.append({
                                "pricelistid" : price_list["id"]
                                ,"pricelistname": price_list["name"]["text"]
                                ,"code" : price_list["code"]
                                ,"currencycode" : price_list["currencyCode"]
                                ,"pricelisttypecode" : price_list["priceListTypeCode"]
                                ,"gross" : price_list["gross"]
                                ,"createdon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                                ,"updatedon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                        })

            elif self.entity is BrightpearlModule.CONTACT:

                for contact in list_with_details:

                    entities_to_insert.append({
                                "contactid" : contact["contactId"]
                                ,"firstname": contact["firstName"]
                                ,"lastname": contact["lastName"]
                                ,"countryiso" : contact["postalAddresses"][0]["countryIsoCode"] if "postalAddresses" in contact else "NA"
                                ,"email" : contact["communication"]["emails"]["PRI"]["email"] if "PRI" in contact["communication"]["emails"] else "NA"
                                ,"createdon": contact["createdOn"]
                                ,"updatedon": contact["updatedOn"] if "updatedOn" in contact else contact["createdOn"]
                                ,"companyid":contact["companyId"] if "companyId" in contact else 0
                                ,"creditlimit":contact["financialDetails"]["creditLimit"] if "creditLimit" in contact["financialDetails"] else 0
                                ,"currencyid":contact["financialDetails"]["currencyId"] if "currencyId" in contact["financialDetails"] else 0
                                ,"organisationid": contact["organisation"]["organisationId"] if "organisationId" in contact["organisation"] else 0
                                ,"organisationname": contact["organisation"]["name"] if "name" in contact["organisation"] else "NA"
                                ,"contacttags": contact["contactTags"] if "contactTags" in contact and contact["contactTags"]!="" else "NA"
                        }) 
                        
            elif self.entity is BrightpearlModule.COMPANY:

                for company in list_with_details:
                   
                    entities_to_insert.append({
                                "companyid" : company["id"] if "id" in company else 0
                                ,"companyname":company["name"] if "name" in company else "NA"
                                ,"createdon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                                ,"updatedon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                                
                               
                        })
            
            elif self.entity is BrightpearlModule.CUSTOMERPAYMENT:

                for cus in list_with_details:
                    print(cus)
                    for values in cus['results']:
                            entities_to_insert.append({
                                "paymentid" :values[0],
                                "transactionref" :values[1],
                                "transactioncode" :values[2],
                                "paymentmethodcode" :values[3],
                                "paymenttype" :values[4],
                                "orderid" :values[5],
                                "currencyid" :values[6],
                                "currencycode" :values[7],
                                "amountauthorized" :values[8],
                                "amountpaid" :values[9],
                                "expires" :values[10],
                                "paymentdate" :values[11],
                                "createdon" :values[12],
                                "journalid" :values[13],
                                "updatedon": values[12]


                                })
            
            elif self.entity is BrightpearlModule.TAGS:

                for tag in list_with_details:
                    for key, value in tag.items():
                        
                        entities_to_insert.append({
                                "tagid" : value["tagId"] if "tagId" in value else 0
                                ,"tagname":value["tagName"] if "tagName" in value else "NA"
                                ,"createdon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                                ,"updatedon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                                
                               
                                
                               
                            })                        
                        
            elif self.entity is BrightpearlModule.BRIGHTPEARLCATEGORY:

                for category in list_with_details:

                    entities_to_insert.append({
                                "brightpearlcategoryid" : category["id"]
                                ,"brightpearlcategoryname": category["name"]
                                ,"parentid" : category["parentId"]
                                ,"active" : category["active"]
                                ,"description" : category["description"]["text"] if "text" in category["description"] else "N/A"
                                ,"createdon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                                ,"updatedon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                        })

            elif self.entity is BrightpearlModule.SEASON:
                             
                for season in list_with_details:

                    entities_to_insert.append({
                                "seasonid" : season["id"]
                                ,"seasonname": season["name"]
                                ,"datefrom" : season["dateFrom"] if "dateFrom" in season else "1970-01-01"
                                ,"dateto" : season["dateTo"] if "dateTo" in season else "9999-01-01"
                                ,"seasondescription" : season["description"] if "description" in season else "N/A"
                                ,"createdon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                                ,"updatedon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                        })                                           

            elif self.entity is BrightpearlModule.ORDER:

                for order in list_with_details:

                    entities_to_insert.append({
                                "orderid": order["id"]
                                ,"parentorderdid": order["parentOrderId"]
                                ,"ordertypecode": order["orderTypeCode"]
                                ,"orderstatus": order["orderStatus"]["name"] if "name" in order["orderStatus"] else "N/A"
                                ,"reference": order["reference"]
                                ,"tax": order["state"]["tax"]
                                ,"acknowledged": False if order["acknowledged"] == 0 else True
                                ,"orderpaymentstatus": order["orderPaymentStatus"]
                                ,"stockstatuscode": order["stockStatusCode"]
                                ,"allocationstatuscode": order["allocationStatusCode"]
                                ,"shippingstatuscode" : order["shippingStatusCode"]
                                ,"shippingmethodid" : order["delivery"]["shippingMethodId"]
                                ,"accountingcurrencycode": order["currency"]["accountingCurrencyCode"] if "accountingCurrencyCode" in order else order["currency"]["orderCurrencyCode"]
                                ,"exchangerate" : order["currency"]["exchangeRate"]
                                ,"placedon" : order["placedOn"] if "createdOn" in order else order["createdOn"]
                                ,"closedon" : order["closedOn"] if "closedOn" in order else "1970-01-01T00:00:00"
                                ,"deliverydate" : order["delivery"]["deliveryDate"] if "deliveryDate" in order["delivery"] else "1970-01-01T00:00:00"
                                ,"createdbyid" : order["createdById"]
                                ,"totalvaluenet" : order["totalValue"]["net"]
                                ,"taxamount" : order["totalValue"]["taxAmount"]
                                ,"basenet" : order["totalValue"]["baseNet"]
                                ,"basetaxamount" : order["totalValue"]["baseTaxAmount"]
                                ,"basetotal" : order["totalValue"]["baseTotal"]
                                ,"total" : order["totalValue"]["total"]
                                ,"createdon": order["createdOn"]
                                ,"updatedon": order["updatedOn"] if "updatedOn" in order else order["createdOn"]
                                ,"fkcontactid": order["parties"]["customer"]["contactId"] if "customer" in order["parties"] else 0
                                ,"country": order["parties"]["customer"]["country"] if "customer" in order["parties"] and "country" in order["parties"]["customer"] else "NA"
                                ,"taxdate": order["invoices"][0]["taxDate"] if ["invoices"][0] in order else "1970-01-01 00:00:00"
                                ,"invoiceduedate": order["invoices"][0]["dueDate"] if ["invoices"][0] in order else "1970-01-01 00:00:00"
                                ,"invoicerefno": order["invoices"][0]["invoiceReference"] if ["invoices"][0] in order else ""
                                ,"channelid": order["assignment"]["current"]["channelId"] if "channelId" in order["assignment"]["current"] else 0
                                ,"warehouseid":order["warehouseId"] if "warehouseId" in order else ""
                                ,"deliverycountry": order["parties"]["delivery"]["country"] if "delivery" in order["parties"] and "country" in order["parties"]["delivery"] else "NA"
                                ,"billingcountry": order["parties"]["billing"]["country"] if "billing" in order["parties"] and "country" in order["parties"]["billing"] else "NA"
                                
                        })

            elif self.entity is BrightpearlModule.ORDERITEM:

                try:

                    for order in list_with_details:

                        for order_item in order["orderRows"]:

                            if "productOptions" not in order["orderRows"][order_item]:

                                    entities_to_insert.append({
                                                "fkorderid": order["id"]
                                                ,"orderitemid": order_item
                                                ,"dborderitemoptionid": str(order_item) + "|" + str(0)
                                                ,"fkproductid":order["orderRows"][order_item]["productId"]
                                                ,"quantity": int(float(order["orderRows"][order_item]["quantity"]["magnitude"]))
                                                ,"itemcost": order["orderRows"][order_item]["itemCost"]["value"]
                                                ,"taxcode" : order["orderRows"][order_item]["rowValue"]["taxCode"]
                                                ,"taxrate" : order["orderRows"][order_item]["rowValue"]["taxRate"]
                                                ,"itemnet" : order["orderRows"][order_item]["rowValue"]["rowNet"]["value"]
                                                ,"itemtax" : order["orderRows"][order_item]["rowValue"]["rowTax"]["value"]
                                                ,"productoptionname" : "NA"
                                                ,"productoptionvalue" : 0
                                                ,"currencycode" : order["orderRows"][order_item]["rowValue"]["rowNet"]["currencyCode"]
                                                ,"createdon": order["createdOn"]
                                                ,"updatedon": order["updatedOn"] if "updatedOn" in order else order["createdOn"]
                                        }) 

                            else:
                                                    
                                for order_item_option in order["orderRows"][order_item]["productOptions"]:

                                    order_item_option_value = str(order["orderRows"][order_item]["productOptions"][order_item_option])

                                    entities_to_insert.append({
                                                "fkorderid": order["id"]
                                                ,"orderitemid": order_item
                                                ,"dborderitemoptionid": str(order_item) + "|" + order_item_option_value
                                                ,"fkproductid":order["orderRows"][order_item]["productId"]
                                                ,"quantity": int(float(order["orderRows"][order_item]["quantity"]["magnitude"]))
                                                ,"itemcost": order["orderRows"][order_item]["itemCost"]["value"]
                                                ,"taxcode" : order["orderRows"][order_item]["rowValue"]["taxCode"]
                                                ,"taxrate" : order["orderRows"][order_item]["rowValue"]["taxRate"]
                                                ,"itemnet" : order["orderRows"][order_item]["rowValue"]["rowNet"]["value"]
                                                ,"itemtax" : order["orderRows"][order_item]["rowValue"]["rowTax"]["value"]
                                                ,"productoptionname" : order_item_option
                                                ,"productoptionvalue" : order_item_option_value
                                                ,"currencycode" : order["orderRows"][order_item]["rowValue"]["rowNet"]["currencyCode"]
                                                ,"createdon": order["createdOn"]
                                                ,"updatedon": order["updatedOn"] if "updatedOn" in order else order["createdOn"]
                                        })
                except TypeError as k:

                    next               

            elif self.entity is BrightpearlModule.PRODUCT:
                
                for product in list_with_details:

                    #each product has its own variation. We need to parse through and insert this variations.
                    if "variations" not in product:

                        entities_to_insert.append({
                                        "dbproductidoptionvalue": str(product["id"]) + "|" + str(0)
                                        ,"productid": product["id"]
                                        ,"fkbrandid": product["brandId"]
                                        ,"fkoptionvalueid" : 0        
                                        ,"optionname": ""         
                                        ,"fkproducttypeid": product["productTypeId"] if product["productTypeId"] != 0 else 1
                                        ,"fkbrightpearlcategoryid": product["salesChannels"][0]["categories"][0]["categoryCode"]
                                        ,"fkseasonid": product["seasonIds"][0] if len(product["seasonIds"]) > 0 else 0
                                        ,"sku": product["identity"]["sku"]
                                        ,"mpn":  product["identity"]["mpn"] if "mpn" in product["identity"] else ''
                                        ,"ean": product["identity"]["ean"] if "ean" in product["identity"] else ''
                                        ,"barcode": product["identity"]["barcode"]
                                        ,"featured": product["featured"]
                                        ,"saleschannelname": product["salesChannels"][0]["salesChannelName"]
                                        ,"productname": product["salesChannels"][0]["productName"]
                                        ,"productcondition": product["salesChannels"][0]["productCondition"]
                                        ,"status": product["status"]
                                        ,"createdon": product["createdOn"]
                                        ,"updatedon": product["updatedOn"] if "updatedOn" in product else product["createdOn"]
                                        ,"dimensionslength" : product["stock"]["dimensions"]["length"]
                                        ,"dimensionsheight" : product["stock"]["dimensions"]["height"]
                                        ,"dimensionswidth" : product["stock"]["dimensions"]["width"]
                                        ,"dimensionsvolume" : product["stock"]["dimensions"]["volume"]
                                })

                    else:
                    
                        for variation in product["variations"]:

                            entities_to_insert.append({
                                        "dbproductidoptionvalue": str(product["id"]) + "|" + str(variation["optionValueId"])
                                        ,"productid": product["id"]
                                        ,"fkbrandid": product["brandId"]
                                        ,"fkoptionvalueid" : variation["optionValueId"]         
                                        ,"optionname": variation["optionName"]         
                                        ,"fkproducttypeid": product["productTypeId"] if product["productTypeId"] != 0 else 1
                                        ,"fkbrightpearlcategoryid": product["salesChannels"][0]["categories"][0]["categoryCode"]
                                        ,"fkseasonid": product["seasonIds"][0] if len(product["seasonIds"]) > 0 else 0
                                        ,"sku": product["identity"]["sku"]
                                        ,"mpn":  product["identity"]["mpn"] if "mpn" in product["identity"] else ''
                                        ,"ean": product["identity"]["ean"] if "ean" in product["identity"] else ''
                                        ,"barcode": product["identity"]["barcode"]
                                        ,"featured": product["featured"]
                                        ,"saleschannelname": product["salesChannels"][0]["salesChannelName"]
                                        ,"productname": product["salesChannels"][0]["productName"]
                                        ,"productcondition": product["salesChannels"][0]["productCondition"]
                                        ,"status": product["status"]
                                        ,"createdon": product["createdOn"]
                                        ,"updatedon": product["updatedOn"] if "updatedOn" in product else product["createdOn"]
                                        ,"dimensionslength" : product["stock"]["dimensions"]["length"]
                                        ,"dimensionsheight" : product["stock"]["dimensions"]["height"]
                                        ,"dimensionswidth" : product["stock"]["dimensions"]["width"]
                                        ,"dimensionsvolume" : product["stock"]["dimensions"]["volume"]
                                })                

            elif self.entity is BrightpearlModule.PRODUCTPRICE:

                try:
                
                    for product_price in list_with_details:
                        
                        #each product has its own variation. We need to parse through and insert this variations.
                        if product_price["productId"] == 1000 or product_price["productId"] == 1001:

                            next

                        else:
                        
                            for price_list in product_price["priceLists"]:

                                for price in price_list["quantityPrice"]:
                                    
                                    entities_to_insert.append({
                                        "dbproductpricevalue": str(product_price["productId"]) + "|" + price + "|" + str(price_list["priceListId"])
                                        ,"fkproductid":product_price["productId"]
                                        ,"fkpricelistid":price_list["priceListId"]
                                        ,"quantitypricenumber": price
                                        ,"quantitypricevalue": price_list["quantityPrice"][price]
                                        ,"createdon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                                        ,"updatedon": datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                                    })

                except TypeError as k:

                    self.log.error(k)
                    next

            return entities_to_insert                

    def entity_soft_delete (self):

        """
        This method will handle the entity selected in the object and by using the SEARCH
        request. It will search the current pks in brightpearl and ocmpare with the ones that
        exist in the database. The ones that exist in the database and not in brightpearl will be
        UPDATE and marked as deleted. No hard deletes are done. For the time being this will only be applies to products. 
        This verification will be done once a day at midnight.
        """
        
        time_now = datetime.now().time()
        start_time = datetime.time(datetime(1970,1,1,00,20,00))
        end_time = datetime.time(datetime(1970,1,1,00,59,00)) 
       
        if time_now >= start_time: #and time_now < end_time:

           
            #self.log.info("Soft delete check start to {0} for {1}".format(self.entity_name, self.brightpearl_api_interface.schema_to_handle))

            db1 = PostgresInteraction(self.log, self.db_context
                ,self.brightpearl_api_interface.schema_to_handle, self.entity)

            # List of ids from brightpearl
            list_of_ids_brightpearl = self.brightpearl_api_interface.get_ids_from_entity(self.entity,"1970-01-01T00:00:01",db1)
            
            # List of ids in the database
            list_of_ids_database = db1.get_ids_on_timestamp("1970-01-01 00:00:01") # This way we'll get all the ids that exist in the db that weren't deleted yet
            #print("database ids",list_of_ids_database)
            ids_to_delete = self.__get_ids_to_delete(list_of_ids_brightpearl, list_of_ids_database)
            #print(ids_to_delete)
            #self.log.info("Soft deleting {0} ids from {1}. Ids: {2}".format(str(len(ids_to_delete)),str(self.entity_name),str(ids_to_delete)))

            if len(ids_to_delete) > 0:

                db1.update_deleted_entities(ids_to_delete)

            else:

                self.log.info("Nothing to delete in {0}".format(self.entity_name))

        







