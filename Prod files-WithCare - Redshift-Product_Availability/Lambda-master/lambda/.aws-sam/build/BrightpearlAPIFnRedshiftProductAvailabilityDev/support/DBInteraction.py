import psycopg2
import psycopg2.extras as pe
from psycopg2 import sql, connect
import boto3
from datetime import datetime
import json
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

class PostgresInteraction:
    
    def __init__(self, logger, db_context, db_schema=None, entity=None):
        
        self.log = logger
        
        try:

            host = db_context["db_host"]

            user = db_context["db_user"]

            password = db_context["db_user_pass"]

            database = db_context["db_database"]            

            self.db_schema = db_schema
            
            db_port = db_context["db_port"]  
            
            self.log.debug(host + " " + user + " " + password + " " + str(database) + " " + str(db_schema)+ " " + str(db_port))
            
            self.conn = psycopg2.connect(host=host, user=user, password=password, database=database, port=db_port)
            
            self.cursor = self.conn.cursor()
            
            self.log.info("Connected to host " + host + " to DB " + database)
            
            self.entity = entity
            
            # self.columns_name = self.get_columns_names()
                
            
        except psycopg2.Error as e:
            
            self.log.error("Error while connectiong to the DB: " + str(e))
            
            if self.conn.closed == 0:
                
                self.conn.close()
                
    #inserts data in products table - requires a list of dicts with query params as key and product values as dict values
    
    def insert_date_in_bulk (self, list_with_data):

        try:

            entity_id = self.entity.value["databaseId"].lower()
            entity_table = self.entity.value["table_name"]            
            

            if len(list_with_data) > 0:

                entity_table_columns_list = list_with_data[0].keys()

                insert_sql = sql.SQL("INSERT INTO {schema}.{table} ({columns}) VALUES ({data})").format(
                    schema=sql.Identifier(self.db_schema)
                    ,table=sql.Identifier(entity_table)
                    ,columns=sql.SQL(",").join(sql.Identifier(c) for c in entity_table_columns_list)
                    ,data=sql.SQL(",").join(sql.Placeholder(c) for c in entity_table_columns_list)
                )

                truncate_qry = "TRUNCATE TABLE " + self.db_schema + "." + entity_table + ";"
                
                
                self.cursor.execute(truncate_qry)
                self.conn.commit()
                

                dataFrameHistorical = pd.DataFrame()
                id_list = []
                # for item in list_with_data:
                    
                #     # dfItem = pd.json_normalize(item)
                #     # dataFrameHistorical = dataFrameHistorical.append(dfItem, ignore_index=True) 
                #     id_to_check = str(item[entity_id])
                #     id_list.append(id_to_check)
                #     product_to_check = {entity_id:str(item[entity_id])}
                #     #item['updatedon'] = str(item['updatedon'])[:-1].replace("T", " ")
                #     #item['createdon'] = str(item['createdon'])[:-1].replace("T", " ")
                    

                # engine = create_engine("postgresql+psycopg2://{user}:{pw}@dev-vvastdb.cluster-cxrw91hvdsiz.eu-west-2.rds.amazonaws.com:5432/{db}"
                       # .format(user="vvast_admin",
                               # pw="FqZ0jwVO3Z",
                               # db="dev_vvast"))
                # engine = create_engine("redshift+psycopg2://{user}:{pw}@redshift-cluster-1-dev.ctaiorf9vo0h.eu-west-2.redshift.amazonaws.com:5439/{db}"
                       # .format(user="dwhuserdev",
                               # pw="djfaksfkjj456kjkD",
                               # db="dwh_dev"))
                engine = create_engine("redshift+psycopg2://{user}:{pw}@redshift-cluster-prod.ctaiorf9vo0h.eu-west-2.redshift.amazonaws.com:5439/{db}"
                       .format(user="dwhuserprod",
                               pw="iP4VjT^1rOFE4lPok&xw3S1N%uofc8",
                               db="dwh_prod"))
                
                # dataFrameHistorical = pd.json_normalize(list_with_data)
                dataFrameHistorical = pd.DataFrame(list_with_data, dtype=object)
                print(dataFrameHistorical)
                print("=================================================================================")
                print(datetime.now())
                # dataFrameHistorical.to_sql(entity_table, con = engine, if_exists = 'append',schema = self.db_schema, index=False, method = 'multi', chunksize=5000)
                s3_session = boto3.Session(
                aws_access_key_id = "AKIA3IELB2EMF4DEC5FM",
                aws_secret_access_key = "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"
                )
                STAGING_BUCKET = "redshift-s3-dataloading-prod"
                STAGING_PREFIX = self.db_schema
                STAGING_FILENAME = entity_table + ".csv"
                s3_path = "s3://{bucket}/{folder}/{filename}".format(bucket=STAGING_BUCKET,folder=STAGING_PREFIX,filename=STAGING_FILENAME)
                # s3_path = "s3://dwh-etl-dev/" + entity_table +".csv"
                local_stage = "/tmp/" + entity_table + ".csv"
                ## Put this where you create connection to redshift
                # preferebly outside the lambda handler
                s3_client = boto3.client('s3')
                # Save the dataframe to a local file in lambda storage
                dataFrameHistorical.to_csv(local_stage, index=False)
                ## Upload the file to your bucket
                # Remember what i mentioned about folders in s3
                #    Key in s3 is basically a filename
                #    s3 GUI shows prefexes as folders
                #    So to put a file inside a folder
                #    Add it to the start of the Key
                bucket_name = 'redshift-s3-dataloading-prod'
                key = STAGING_PREFIX + "/" + STAGING_FILENAME
                # key = 'folder/filename.csv'
                ## Call upload_file() on the local file
                # boto3 does multipart concurrent upload for large files
                # automatically, so this call can be used anywhere
                s3_client.upload_file(
                    Filename=local_stage,
                    Bucket=bucket_name,
                    Key=key
                )
                # wr.s3.to_csv(
                # df=dataFrameHistorical,
                # path=s3_path,
                # boto3_session=s3_session,
                # index=False
                # )

                COPY_AUTH_ROLE_ARN = "arn:aws:iam::773385736472:role/AmazonS3RedShift"

                COPY_STMT = f"""COPY {self.db_schema}.{entity_table} ({",".join(dataFrameHistorical.columns)})
                            FROM '{s3_path}'
                            IAM_ROLE '{COPY_AUTH_ROLE_ARN}'
                            CSV
                            DELIMITER ','
                            IGNOREHEADER 1
                            EMPTYASNULL
                            ACCEPTANYDATE
                            dateformat AS 'auto'
                            timeformat AS 'auto'
                            ;"""


                url = URL.create(
                    drivername='redshift+psycopg2',
                    host="redshift-cluster-prod.ctaiorf9vo0h.eu-west-2.redshift.amazonaws.com",
                    port=5439,
                    database="dwh_prod",
                    username="dwhuserprod",
                    password="iP4VjT^1rOFE4lPok&xw3S1N%uofc8"
                )
                prod_redshift = create_engine(url)
                with prod_redshift.begin() as trans:
                    trans.execute(COPY_STMT)
                print(datetime.now())
                print("=================================================================================")
                self.log.info(str(len(list_with_data)) + " rows inserted / updated.")
                
                self.cursor.close()
            else:

                self.log.info("Nothing to persist")
                
        except psycopg2.ProgrammingError as pg:
            
            self.conn.rollback()
            
            if self.conn.closed == 0:
                
                self.conn.close()

            self.log.error("Error in sql: " + str(pg))

    
    def insert_data_into_db_with_deletes (self, list_with_data):

        try:

            entity_id = self.entity.value["databaseId"].lower()
            entity_table = self.entity.value["table_name"]            
            

            if len(list_with_data) > 0:

                entity_table_columns_list = list_with_data[0].keys()
        
                test_if_item_exists = "SELECT count(*) FROM "+ self.db_schema +"."+entity_table+" WHERE "+entity_id+" = %("+entity_id+")s;"

                insert_statement = sql.SQL("INSERT INTO {schema}.{table} ({columns}) VALUES ({data})").format(
                    schema=sql.Identifier(self.db_schema)
                    ,table=sql.Identifier(entity_table)
                    ,columns=sql.SQL(",").join(sql.Identifier(c) for c in entity_table_columns_list)
                    ,data=sql.SQL(",").join(sql.Placeholder(c) for c in entity_table_columns_list)
                )

                delete_statement = sql.SQL("DELETE FROM {schema}.{table} WHERE {entity_id} = {id}").format(
                    schema=sql.Identifier(self.db_schema)
                    ,table=sql.Identifier(entity_table)
                    ,entity_id=sql.Identifier(entity_id)
                    ,id=sql.Placeholder(entity_id)
                )

                #self.log.debug(insert_statement.as_string(self.conn) + " " + delete_statement.as_string(self.conn))
                
                dataFrameHistorical = pd.DataFrame()
                id_list = []
                for item in list_with_data:
                    
                    # dfItem = pd.json_normalize(item)
                    # dataFrameHistorical = dataFrameHistorical.append(dfItem, ignore_index=True) 
                    id_to_check = str(item[entity_id])
                    id_list.append(id_to_check)
                    product_to_check = {entity_id:str(item[entity_id])}
                    #item['updatedon'] = str(item['updatedon'])[:-1].replace("T", " ")
                    #item['createdon'] = str(item['createdon'])[:-1].replace("T", " ")
                
                # dataFrameHistorical = pd.json_normalize(list_with_data)
                dataFrameHistorical = pd.DataFrame(list_with_data, dtype=object)
                print(dataFrameHistorical)
                print('-----------------------------------------------------------')
                print(datetime.now())
                dlt_qry = "delete from " + self.db_schema + "." + entity_table + " where " + entity_id + " in (%s)" % ','.join(["%s"] * len(id_list))
                self.cursor.execute(dlt_qry, id_list)
                self.conn.commit()
                print(datetime.now())
                print('-----------------------------------------------------------')

                # engine = create_engine("postgresql+psycopg2://{user}:{pw}@dev-vvastdb.cluster-cxrw91hvdsiz.eu-west-2.rds.amazonaws.com:5432/{db}"
                       # .format(user="vvast_admin",
                               # pw="FqZ0jwVO3Z",
                               # db="dev_vvast"))
                # engine = create_engine("redshift+psycopg2://{user}:{pw}@redshift-cluster-1-dev.ctaiorf9vo0h.eu-west-2.redshift.amazonaws.com:5439/{db}"
                       # .format(user="dwhuserdev",
                               # pw="djfaksfkjj456kjkD",
                               # db="dwh_dev"))
                engine = create_engine("redshift+psycopg2://{user}:{pw}@redshift-cluster-prod.ctaiorf9vo0h.eu-west-2.redshift.amazonaws.com:5439/{db}"
                       .format(user="dwhuserprod",
                               pw="iP4VjT^1rOFE4lPok&xw3S1N%uofc8",
                               db="dwh_prod"))
                
                print("=================================================================================")
                print(datetime.now())
                # dataFrameHistorical.to_sql(entity_table, con = engine, if_exists = 'append',schema = self.db_schema, index=False, method = 'multi', chunksize=100000)
                s3_session = boto3.Session(
                aws_access_key_id = "AKIA3IELB2EMF4DEC5FM",
                aws_secret_access_key = "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"
                )
                STAGING_BUCKET = "redshift-s3-dataloading-prod"
                STAGING_PREFIX = self.db_schema
                STAGING_FILENAME = entity_table + ".csv"
                s3_path = "s3://{bucket}/{folder}/{filename}".format(bucket=STAGING_BUCKET,folder=STAGING_PREFIX,filename=STAGING_FILENAME)
                # s3_path = "s3://dwh-etl-dev/" + entity_table +".csv"
                local_stage = "/tmp/" + entity_table + ".csv"
                ## Put this where you create connection to redshift
                # preferebly outside the lambda handler
                s3_client = boto3.client('s3')
                # Save the dataframe to a local file in lambda storage
                dataFrameHistorical.to_csv(local_stage, index=False)
                ## Upload the file to your bucket
                # Remember what i mentioned about folders in s3
                #    Key in s3 is basically a filename
                #    s3 GUI shows prefexes as folders
                #    So to put a file inside a folder
                #    Add it to the start of the Key
                bucket_name = 'redshift-s3-dataloading-prod'
                key = STAGING_PREFIX + "/" + STAGING_FILENAME
                # key = 'folder/filename.csv'
                ## Call upload_file() on the local file
                # boto3 does multipart concurrent upload for large files
                # automatically, so this call can be used anywhere
                s3_client.upload_file(
                    Filename=local_stage,
                    Bucket=bucket_name,
                    Key=key
                )
                # wr.s3.to_csv(
                # df=dataFrameHistorical,
                # path=s3_path,
                # boto3_session=s3_session,
                # index=False
                # )


                COPY_AUTH_ROLE_ARN = "arn:aws:iam::773385736472:role/AmazonS3RedShift"

                COPY_STMT = f"""COPY {self.db_schema}.{entity_table} ({",".join(dataFrameHistorical.columns)})
                            FROM '{s3_path}'
                            IAM_ROLE '{COPY_AUTH_ROLE_ARN}'
                            CSV
                            DELIMITER ','
                            IGNOREHEADER 1
                            EMPTYASNULL
                            ACCEPTANYDATE
                            dateformat AS 'auto'
                            timeformat AS 'auto'
                            ;"""


                url = URL.create(
                    drivername='redshift+psycopg2',
                    host="redshift-cluster-prod.ctaiorf9vo0h.eu-west-2.redshift.amazonaws.com",
                    port=5439,
                    database="dwh_prod",
                    username="dwhuserprod",
                    password="iP4VjT^1rOFE4lPok&xw3S1N%uofc8"
                )
                prod_redshift = create_engine(url)
                with prod_redshift.begin() as trans:
                    trans.execute(COPY_STMT)
                print(datetime.now())
                print("=================================================================================")
                self.log.info(str(len(list_with_data)) + " rows inserted / updated.")
                
                self.cursor.close()
            else:

                self.log.info("Nothing to persist")
                
        except psycopg2.ProgrammingError as pg:
            
            self.conn.rollback()
            
            if self.conn.closed == 0:
                
                self.conn.close()

            self.log.error("Error in sql: " + str(pg))

    def insert_data_into_db (self, list_with_data):
        
        try:

            entity_id = self.entity.value["databaseId"].lower()
            entity_table = self.entity.value["table_name"]            
            

            if len(list_with_data) > 0:

                entity_table_columns_list = list_with_data[0].keys()
        
                test_if_item_exists = "SELECT count(*) FROM "+ self.db_schema +"."+entity_table+" WHERE "+entity_id+" = %("+entity_id+")s;"

                product_merge_sql = sql.SQL("INSERT INTO {schema}.{table} ({columns}) VALUES ({data})").format(
                    schema=sql.Identifier(self.db_schema)
                    ,table=sql.Identifier(entity_table)
                    ,columns=sql.SQL(",").join(sql.Identifier(c) for c in entity_table_columns_list)
                    ,data=sql.SQL(",").join(sql.Placeholder(c) for c in entity_table_columns_list)
                )

                delete_statement = sql.SQL("DELETE FROM {schema}.{table} WHERE {entity_id} = {id}").format(
                    schema=sql.Identifier(self.db_schema)
                    ,table=sql.Identifier(entity_table)
                    ,entity_id=sql.Identifier(entity_id)
                    ,id=sql.Placeholder(entity_id)
                )

                #self.log.debug(product_merge_sql.as_string(self.conn) + " " + product_update_sql.as_string(self.conn))
 
                #dataFrameHistorical = pd.DataFrame()
                id_list = []
                for item in list_with_data:
                    
                    # dfItem = pd.json_normalize(item)
                    # dataFrameHistorical = dataFrameHistorical.append(dfItem, ignore_index=True) 
                    id_to_check = str(item[entity_id])
                    id_list.append(id_to_check)
                    product_to_check = {entity_id:str(item[entity_id])}
                    # print(item)
                    #item['updatedon'] = str(item['updatedon'])[:-1].replace("T", " ")
                    #item['createdon'] = str(item['createdon'])[:-1].replace("T", " ")

                
                # dataFrameHistorical = pd.json_normalize(list_with_data)
                dataFrameHistorical = pd.DataFrame(list_with_data, dtype=object)
                
                # dataFrameHistorical['rowimportdate'] = row_import_list
                # dataFrameHistorical['isdeleted'] = isdeleted_lst
                print(dataFrameHistorical)
                print('-----------------------------------------------------------')
                print(datetime.now())
                dlt_qry = "delete from " + self.db_schema + "." + entity_table + " where " + entity_id + " in (%s)" % ','.join(["%s"] * len(id_list))
                self.cursor.execute(dlt_qry, id_list)
                self.conn.commit()
                print(datetime.now())
                print('-----------------------------------------------------------')

                # engine = create_engine("postgresql+psycopg2://{user}:{pw}@dev-vvastdb.cluster-cxrw91hvdsiz.eu-west-2.rds.amazonaws.com:5432/{db}"
                       # .format(user="vvast_admin",
                               # pw="FqZ0jwVO3Z",
                               # db="dev_vvast"))
                # engine = create_engine("redshift+psycopg2://{user}:{pw}@redshift-cluster-1-dev.ctaiorf9vo0h.eu-west-2.redshift.amazonaws.com:5439/{db}"
                       # .format(user="dwhuserdev",
                               # pw="djfaksfkjj456kjkD",
                               # db="dwh_dev"))
                engine = create_engine("redshift+psycopg2://{user}:{pw}@redshift-cluster-prod.ctaiorf9vo0h.eu-west-2.redshift.amazonaws.com:5439/{db}"
                       .format(user="dwhuserprod",
                               pw="iP4VjT^1rOFE4lPok&xw3S1N%uofc8",
                               db="dwh_prod"))
                
                # table_name = self.entity.value["table_name"]
                # db_schema = self.db_schema
                # print(db_schema)
        
                # columns_qry = "SELECT COLUMN_NAME FROM information_schema.columns "  + "WHERE table_schema = '" + db_schema + "' and table_name = '" + table_name + "' order by ordinal_position;" 
                
                # print(columns_qry)
                # self.cursor.execute(columns_qry)
                
                # columns_to_process = [item[0] for item in self.cursor.fetchall()]
                
                # self.log.debug(columns_to_process)
                
                # print(columns_to_process)
                print("=================================================================================")
                print(datetime.now())
                # dataFrameHistorical = dataFrameHistorical[columns_to_process]
                # dataFrameHistorical.to_sql(entity_table, con = engine, if_exists = 'append',schema = self.db_schema, index=False, method = 'multi', chunksize=100000)
                # dataFrameHistorical = dataFrameHistorical.createdon.str.rstrip('Z')
                s3_session = boto3.Session(
                aws_access_key_id = "AKIA3IELB2EMF4DEC5FM",
                aws_secret_access_key = "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"
                )
                STAGING_BUCKET = "redshift-s3-dataloading-prod"
                STAGING_PREFIX = self.db_schema
                STAGING_FILENAME = entity_table + ".csv"
                s3_path = "s3://{bucket}/{folder}/{filename}".format(bucket=STAGING_BUCKET,folder=STAGING_PREFIX,filename=STAGING_FILENAME)
                # s3_path = "s3://dwh-etl-dev/" + entity_table +".csv"
                local_stage = "/tmp/" + entity_table + ".csv"
                ## Put this where you create connection to redshift
                # preferebly outside the lambda handler
                s3_client = boto3.client('s3')
                # Save the dataframe to a local file in lambda storage
                dataFrameHistorical.to_csv(local_stage, index=False)
                ## Upload the file to your bucket
                # Remember what i mentioned about folders in s3
                #    Key in s3 is basically a filename
                #    s3 GUI shows prefexes as folders
                #    So to put a file inside a folder
                #    Add it to the start of the Key
                bucket_name = 'redshift-s3-dataloading-prod'
                key = STAGING_PREFIX + "/" + STAGING_FILENAME
                # key = 'folder/filename.csv'
                ## Call upload_file() on the local file
                # boto3 does multipart concurrent upload for large files
                # automatically, so this call can be used anywhere
                s3_client.upload_file(
                    Filename=local_stage,
                    Bucket=bucket_name,
                    Key=key
                )
                # wr.s3.to_csv(
                # df=dataFrameHistorical,
                # path=s3_path,
                # boto3_session=s3_session,
                # index=False
                # )

                COPY_AUTH_ROLE_ARN = "arn:aws:iam::773385736472:role/AmazonS3RedShift"

                COPY_STMT = f"""COPY {self.db_schema}.{entity_table} ({",".join(dataFrameHistorical.columns)})
                            FROM '{s3_path}'
                            IAM_ROLE '{COPY_AUTH_ROLE_ARN}'
                            CSV
                            DELIMITER ','
                            IGNOREHEADER 1
                            EMPTYASNULL
                            ACCEPTANYDATE
                            dateformat AS 'auto'
                            timeformat AS 'auto'
                            ;"""


                url = URL.create(
                    drivername='redshift+psycopg2',
                    host="redshift-cluster-prod.ctaiorf9vo0h.eu-west-2.redshift.amazonaws.com",
                    port=5439,
                    database="dwh_prod",
                    username="dwhuserprod",
                    password="iP4VjT^1rOFE4lPok&xw3S1N%uofc8"
                )
                prod_redshift = create_engine(url)
                with prod_redshift.begin() as trans:
                    trans.execute(COPY_STMT)
                print(datetime.now())
                print("=================================================================================")
                self.log.info(str(len(list_with_data)) + " rows inserted / updated.")
                
                self.cursor.close()
            else:

                self.log.info("Nothing to persist")
                
        except psycopg2.ProgrammingError as pg:
            
            self.conn.rollback()
            
            if self.conn.closed == 0:
                
                self.conn.close()

            self.log.error("Error in sql: " + str(pg))
                               
    def get_timestamp_from_table (self):
        
        # This method is used for incremental loads. That way we don't have to pull all the data from the API
        # only the modified data. 
        
        table_name = self.entity.value["table_name"]
        
        timestamp_qry = "SELECT coalesce(max(updatedOn), '1970-01-01 00:00:01') AS maxTimestamp \
            FROM " + self.db_schema + "." + table_name + ";"
        
        try:            
            
            self.cursor.execute(timestamp_qry)
            
            timestamp_to_process = self.cursor.fetchone()
            
            self.log.debug(timestamp_to_process)
            
            return timestamp_to_process[0]
            
        except psycopg2.ProgrammingError as pg:
            
            self.conn.rollback()

            if self.conn.closed == 0:
                
                self.conn.close()
            
            self.log.error("Error in sql: " + str(pg))     
    
    def truncate_tbl(self):
        entity_id = self.entity.value["databaseId"].lower()
        entity_table = self.entity.value["table_name"]
        
        try:
            truncate_qry = "TRUNCATE TABLE " + self.db_schema + "." + entity_table + ";"
            self.cursor.execute(truncate_qry);
            self.conn.commit()
                
        except psycopg2.ProgrammingError as pg:
            
            self.conn.rollback()
    
    def gi_procs (self,schemaname):
        
        try:
            proc=schemaname+".updategoodsinventory";
            self.cursor.callproc(proc,[schemaname]);
            self.conn.commit()
            
        except psycopg2.ProgrammingError as pg:
            
            self.conn.rollback()

            if self.conn.closed == 0:
                
                self.conn.close()
            
            self.log.error("Error in sql: " + str(pg)) 
               
                                
    def get_ids_on_timestamp (self, timestamp_from_late):

        # This method is used in getting a list of ids from a table based on a timestamp.
        
        table_name = self.entity.value["post_filter"]["table_reference"] if self.entity.value["post_filter"] != "" else self.entity.value["table_name"]
        ids_to_get = self.entity.value["post_filter"]["id_reference"] if self.entity.value["post_filter"] != "" else self.entity.value["Id"]
        
        timestamp_qry = "SELECT DISTINCT " + ids_to_get +" AS idsToProc \
            FROM " + self.db_schema + "." + table_name + " WHERE ROWIMPORTDATE >= '" + str(timestamp_from_late) +"' AND isdeleted = False;"
        
        try:

            ids_to_retrieve = []
            
            self.cursor.execute(timestamp_qry)
            
            ids_to_process = self.cursor.fetchall()
            
            self.log.debug(ids_to_process)
            
            for id in ids_to_process:

                ids_to_retrieve.append([id[0]])

            return ids_to_retrieve
            
        except psycopg2.ProgrammingError as pg:
            
            self.conn.rollback()

            if self.conn.closed == 0:
                
                self.conn.close()            
            
            self.log.error("Error in sql: " + str(pg))

    def insert_error_in_table (self, context_dict):

        try:

            log_error_qry = sql.SQL("INSERT INTO {schema}.{table} ({columns}) VALUES ({data})").format(
                        schema=sql.Identifier(self.db_schema)
                        ,table=sql.Identifier("errorlog")
                        ,columns=sql.SQL(",").join(sql.Identifier(c) for c in context_dict)
                        ,data=sql.SQL(",").join(sql.Placeholder(c) for c in context_dict)                    
                    )

            self.cursor.execute(log_error_qry, context_dict)

            self.conn.commit()

        except psycopg2.InterfaceError as ir:

            self.log.error("Database error:" + str(ir))

        except psycopg2.ProgrammingError as pg:
            
            self.conn.rollback()

            self.log.error("Error in sql: " + str(pg))

    def insert_csv_from_ftp (self, csv_file):

        try:
            #csv_file must be a dict
            
            insert_qry = "INSERT INTO countwise.footfall (content_site, content_date, content_time, content_in, content_bypass) \
                VALUES (%(Site)s,%(Date)s,%(Time)s,%(In)s,%(Bypass)s);"
            
            result = self.cursor.executemany(insert_qry, csv_file)
            self.conn.commit()
            
            self.log.info("Inserted: {0}".format(str(len(list(csv_file)))))

        except psycopg2.ProgrammingError as pg:

            self.conn.rollback()

            self.log.error("Error in sql: " + str(pg))

    def update_deleted_entities (self, ids_to_delete): # ids_to_delete is an iterable

        try:

            # this method soft deleted ids from any given entity. For the denormalized table means that a 
            # id from Brightpearl might update several rown in the db.

            str_ids_to_delete = ",".join((str(val) for val in ids_to_delete))

            update_qry = "UPDATE "+self.db_schema+"."+self.entity.value["table_name"]+" SET isDeleted = TRUE" \
                ",rowimportdate = '" + str(datetime.now()) +"'" \
                " WHERE "+self.entity.value["Id"]+" IN ("+str_ids_to_delete+");"
            
            self.log.debug(update_qry)

            self.log.info("Deleting ids: {0}".format(str_ids_to_delete))

            self.cursor.execute(update_qry)
            self.conn.commit()

            self.log.info("Finished soft deletes")

        except psycopg2.ProgrammingError as pg:

            self.conn.rollback()

            self.log.error("Error in sql: " + str(pg) + ". Nothing was deleted.")





