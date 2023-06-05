import pymysql
import pandas as pd
from config import DATABASE 

def connect():
    return pymysql.connect(db=DATABASE["DB_NAME"], user=DATABASE["DB_USERNAME"], passwd=DATABASE["DB_PASSWORD"],
                           host=DATABASE["DB_HOST"],port=DATABASE["DB_PORT"])


def create_tables(path):
    connection=connect()
    cursor=connection.cursor()

    with open(path, 'r') as sql_file:
        for query in sql_file.read().split(";")[:-1]:
            cursor.execute(query)
            
    connection.commit()
    connection.close()
    

def insert(collection_data, collection_name):
    connection=connect()
    cursor=connection.cursor()

    for document in collection_data:
        document.pop("_id")
        query="INSERT INTO %s VALUES %s;" % (collection_name, tuple(document.values()))
        cursor.execute(query)

    connection.commit()
    connection.close()
    

def run_query(query):
    connection=connect()
    cursor=connection.cursor()
    
    cursor.execute(query)

    datarow=[]

    field_names=[i[0] for i in cursor.description]

    records=cursor.fetchall()
    
    for row in records:
        datarow.append(row)

    connection.close()    

    return pd.DataFrame(datarow,columns=field_names)
