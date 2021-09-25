import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy.sql import text
from sqlalchemy import create_engine
import sys


class update_table():
    def __init__(self,DB_URI):
        self.engine=create_engine(DB_URI)
    def update_records(self,sku,name,description):
        '''
        Update existing records based on the 'sku' key
        '''
        update_query="UPDATE updated_table SET name_list=array_append(name_list,"+"'"+name+"'"+"),description_list=array_append(description_list,"+"'"+description+"'"+")Where sku="+"'"+sku+"';"
        # execute all queries
        self.engine.execute(text
               (update_query
                ))
        self.engine.execute(text('''
        DROP TABLE product_list;
        '''))
        self.engine.execute(text('''
        CREATE TABLE product_list AS  (SELECT x.* FROM (SELECT sku,UNNEST(name_list) AS name,UNNEST(description_list) AS description FROM updated_table) x)
        '''))
        self.engine.execute(text('''
        DROP TABLE agg_table;
        '''))
        self.engine.execute(text('''
        CREATE TABLE IF NOT EXISTS agg_table AS
        (Select name, count(sku) from product_list GROUP BY(name));
        '''))
        print("Process Completed!")


if __name__ == '__main__':
    try:
        sku=sys.argv[1]
        name=sys.argv[2]
        description=sys.argv[3]
    except:
        raise Exception("Please check the number of Arguments correctly also run the file using preceding python interpreter")
    load_dotenv()
    DB_URI=os.environ.get('DB_URI')
    update=update_table(DB_URI)
    update.update_records(sku,name,description)
    

    



