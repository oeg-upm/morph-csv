import sys
import psycopg2
import re
import os
def create_and_insert(csvw,sql, sqlFunctions, alters):

    try:
        # Local connection
        con = psycopg2.connect(database="morphcsv", user="w0xter", password="1234", host="127.0.0.1", port="5432")

        #Docker connection
#        con = psycopg2.connect(database="morphcsv", user="user", password="csv", host="postgres")
    except:
        print("I am unable to connect to the database.")
        sys.exit()
    create_schema(sql, con)
    insert_data(csvw, con)
    if(len(sqlFunctions) > 0):
      insert_functions(sqlFunctions, con)
    insert_alters(alters, con)
    con.close()
def create_schema(sql,con):
    cur = con.cursor()
    cur.execute(sql)
    con.commit()

def insert_data(csvw,con):
    #for i, table in enumerate(csvw["tables"]):
    for i,table in enumerate(csvw["tables"]):
        tablename = re.sub(".csv", "", csvw["tables"][i]["url"].split("/")[-1])

        # Insert docker db
        #insert = "COPY " + tablename + " FROM '/tmp/csv/" + tablename + ".csv' with NULL as E'null' CSV HEADER;"

        #Insert local db
        pwd = os.getcwd()
        insert = "COPY "+tablename+" FROM '" + str(pwd) + "/tmp/csv/" + tablename + ".csv' with NULL as E'null' CSV HEADER;"
#        print('Inserting:')
 #       print(insert)
        cur = con.cursor()
        cur.execute(insert)
        con.commit()
def insert_alters(alters, con):
    cur = con.cursor()
    cur.execute(alters)
    con.commit()
def insert_functions(sqlFunctions, con):
#    print('sqlFnuctions: \n' + sqlFunctions)
    cur = con.cursor()
    cur.execute(sqlFunctions)
    con.commit()
