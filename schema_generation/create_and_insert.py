import sys
import psycopg2
import re
import os
def create_and_insert(csvw,sql):
    #con = psycopg2.connect(database="morphcsv", user="user", password="csv", host="127.0.0.1", port="5432")
    try:
        #con = psycopg2.connect(database="morphcsv", user="postgres", password="csv", host="127.0.0.1", port="5432")
        con = psycopg2.connect(database="morphcsv", user="user", password="csv", host="postgres")
    except:
        print("I am unable to connect to the database.")
        sys.exit()
    create_schema(sql, con)
    insert_data(csvw, con)
    con.close()
def create_schema(sql,con):
    cur = con.cursor()
    cur.execute(sql)
    con.commit()

def insert_data(csvw,con):
    #for i, table in enumerate(csvw["tables"]):
    for i,table in enumerate(csvw["tables"]):
        tablename = re.sub(".csv", "", csvw["tables"][i]["url"].split("/")[-1])
        pwd = os.getcwd()
        insert = "COPY " + tablename + " FROM '/tmp/csv/" + tablename + ".csv' with NULL as E'null' CSV HEADER;"
        #insert = "COPY " + tablename + " FROM '/tmp/csv/" + tablename + ".csv' with CSV HEADER;"
        #insert = "COPY "+tablename+" FROM '" + str(pwd) + "/tmp/csv/" + tablename + ".csv' with NULL as E'null' CSV HEADER;"

        cur = con.cursor()
        cur.execute(insert)
        con.commit()

