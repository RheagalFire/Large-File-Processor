import math
from multiprocessing.dummy import Pool as ThreadPool
from sqlalchemy.sql import text
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv



class Read_and_Transform():
    def __init__(self,DB_URI,df_name):
        self.engine = create_engine(DB_URI)
        self.df_name=df_name
    def ingest_data(self):
        '''
        Accordingly Ingest Data Using Chunks.  
        '''
        df=pd.read_csv(self.df_name)
        nworkers = 4 # number of workers that executes insert in parallel fashion
        chunk = math.floor(df.shape[0] / nworkers) # number of chunks
        chunks = [(chunk * i, (chunk * i) + chunk) for i in range(nworkers)]
        chunks.append((chunk * nworkers, df.shape[0]))
        pool = ThreadPool(nworkers)
        self.engine.execute(text('''
        CREATE TABLE IF NOT EXISTS product_list(
            name text,
            sku text,
            description text

        )
        '''))
        def worker(chunk):
            i,j=chunk
            df.iloc[i:j].to_sql("product_list",self.engine,if_exists='append',index=False)
        pool.map(worker,chunks)
        pool.close()
        pool.join()
        print("Data Ingested parallely ")
    def Update_table_creation(self):
        with self.engine.connect() as conn:
            self.engine.execute(text
                               ('''
                               CREATE TABLE IF NOT EXISTS updated_table AS (SELECT sku,array_agg(name) 
                               As name_list,array_agg(description) 
                               As description_list FROM product_list GROUP BY sku);
                               
                               '''))
            try:
                self.engine.execute(text('''
                ALTER TABLE updated_table ADD PRIMARY KEY (sku);
                '''))
            except:
                pass
            print("Updated Table Created Successfully with sku as primary key!")
    def update_existing(self,sku,name,description):
        '''
        Update existing records based on the 'sku' key
        '''
        update_query="UPDATE updated_table SET name_list=array_append(name_list,"+"'"+name+"'"+"),description_list=array_append(description_list,"+"'"+description+"'"+")Where sku="+"'"+sku+"';"
        # Fetch existing Value
        self.engine.execute(text
               (update_query
                ))
        print("Process Completed!")
    def create_aggregate(self):
        '''
        Create an aggregate table on the go.
        '''
        with self.engine.connect() as conn:
            self.engine.execute(text
                               ('''
                               CREATE TABLE IF NOT EXISTS agg_table AS
                               (Select name, count(sku) from product_list GROUP BY(name));
                               '''
                               ))
        print("An Aggregate Table is Created!")
    def create_all_tables(self):
        self.ingest_data()
        self.Update_table_creation()
        self.create_aggregate()



if __name__=="__main__":
    load_dotenv()
    df_name='products.csv'
    DB_URI=os.environ.get('DB_URI')
    object=Read_and_Transform(DB_URI,df_name)
    object.create_all_tables()
