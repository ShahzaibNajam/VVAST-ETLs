import logging
from support.Brightpearl import BrightpearlAPIInteraction, BrightpearlModule, BrightpearlIntegrationInteraction
from support.Secrets import Keys
import json

#setting logging info
logging.basicConfig(format="%(levelname)s;%(message)s;%(asctime)s", datefmt="%Y-%m-%d %H:%M:%S")                
log = logging.getLogger("brightpearl")
log.setLevel(logging.INFO)
                
log.debug("Debug log initialized")
log.info("Script started")

def main(logins_to_handle):
    
    try:
                    
        #instantiates Brightpearl API object and retrieve the secret from AWS secrets
        log.info("Retrieving secrets: prod_brightpearl_integration")
        k1 = Keys()
        brightpearl_secrets = k1.get_keys("prod_brightpearl_integration")
        log.info("Secrets retrieved")
            
            
        #if we are in the debug mode assume it's the local env and don't use the prod DB.
        if log.level == 10:
               
            db_host = "localhost"
            db_user = "brightpearlapp"
            db_user_pass = "EE$pd3#7FY*XJrpG"
            db_database = "vvast"
                
        else:
                
            #Get database credentials as a JSON from secrets - Could have been retrieved from another secret
            #but it's cheaper to reuse the current one.

            conn_context = {"db_host": brightpearl_secrets["prod_rs_db_host"]
                            ,"db_user": brightpearl_secrets["prod_rs_db_user"]
                            ,"db_user_pass":brightpearl_secrets["prod_rs_db_user_pass"]
                            ,"db_database": brightpearl_secrets["prod_rs_db_database"]
                            ,"db_port":5439}

        for schema_to_handle in logins_to_handle:           
            
            log.info("Starting processing for schema: " + schema_to_handle)

            #set the secrets based on the schema to process
            brightpearl_api_key = brightpearl_secrets[schema_to_handle + "_api_key"]
            app_reference = brightpearl_secrets[schema_to_handle + "_reference"]
            app_login = brightpearl_secrets[schema_to_handle + "_login"]

            #instantiate the object that will interface with the API
            b1 = BrightpearlAPIInteraction(log, app_reference, app_login, brightpearl_api_key, schema_to_handle)

            #instantiate the object that will run the entities persistance in the DB. It also needs the Brightpearl API interface
            pl = BrightpearlIntegrationInteraction(log, BrightpearlModule.PRICELIST, b1, conn_context)
            pp = BrightpearlIntegrationInteraction(log, BrightpearlModule.PRODUCTPRICE, b1, conn_context)            
            pt = BrightpearlIntegrationInteraction(log, BrightpearlModule.PRODUCTTYPE, b1 , conn_context)
            pov = BrightpearlIntegrationInteraction(log, BrightpearlModule.PRODUCTOPTIONVALUE, b1 , conn_context)
            b = BrightpearlIntegrationInteraction(log, BrightpearlModule.BRAND, b1, conn_context)
            bc = BrightpearlIntegrationInteraction(log, BrightpearlModule.BRIGHTPEARLCATEGORY, b1, conn_context)
            s = BrightpearlIntegrationInteraction(log, BrightpearlModule.SEASON, b1, conn_context)
            p = BrightpearlIntegrationInteraction(log, BrightpearlModule.PRODUCT, b1, conn_context)
            o = BrightpearlIntegrationInteraction(log, BrightpearlModule.ORDER, b1, conn_context)
            oi = BrightpearlIntegrationInteraction(log, BrightpearlModule.ORDERITEM, b1, conn_context)
            pa = BrightpearlIntegrationInteraction(log, BrightpearlModule.PRODUCTAVAILABILITY, b1, conn_context)
            ch = BrightpearlIntegrationInteraction(log, BrightpearlModule.CHANNEL, b1, conn_context)
            w = BrightpearlIntegrationInteraction(log, BrightpearlModule.WAREHOUSE, b1, conn_context)
            c = BrightpearlIntegrationInteraction(log, BrightpearlModule.CONTACT, b1, conn_context)
            gi = BrightpearlIntegrationInteraction(log, BrightpearlModule.GoodsInventory, b1, conn_context)
            cm= BrightpearlIntegrationInteraction(log, BrightpearlModule.COMPANY, b1, conn_context)
            tg= BrightpearlIntegrationInteraction(log, BrightpearlModule.TAGS, b1, conn_context)
            cp=BrightpearlIntegrationInteraction(log, BrightpearlModule.CUSTOMERPAYMENT, b1, conn_context)
            #process and persist the changes per module.
            gi.persist_module_segment()
            # gi.run_gi_procs ()
            pt.persist_module_segment()
            pl.persist_module_segment()            
            pov.persist_module_segment()
            b.persist_module_segment()
            bc.persist_module_segment()
            s.persist_module_segment()
            p.persist_module_segment()
            c.persist_module_segment()
            o.persist_module_segment()
            ch.persist_module_segment_truncation()
            w.persist_module_segment_truncation()
            # cm.run_truncate_tbl()
            # cm.persist_module_segment()
            #tg.run_truncate_tbl()
            #tg.persist_module_segment()
            if schema_to_handle=='brightpearl_yeti':
                cp.persist_module_segment()
            
            #these must be last to load new values from product
            pp.persist_modules_with_reference()            
            # pa.persist_modules_with_reference()

            oi.persist_module_segment()

            #soft deletes
            #p.entity_soft_delete()
            #o.entity_soft_delete() 
            #gi.entity_soft_delete()

            log.info("Finished processing for schema: " + schema_to_handle)


    except Exception as e:
        
        log.error(e)
        raise e
    
    finally:
        
        log.info("Script finished")

def lambda_handler(event, context):
    
    try:        

        login = event["login"]
        
        main(login)
        
    except Exception as e:
        
        raise e
    
#for debugging purposes won't be called in the lambda
if __name__ == '__main__':
    
    lambda_handler(json.loads("{\"login\": [\"brightpearl_deus\"]}"), "NULL")
