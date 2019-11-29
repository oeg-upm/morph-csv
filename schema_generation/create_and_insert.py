
import psycopg2
import re

def create_and_insert(csvw,sql):
    con = psycopg2.connect(database="morphcsv", user="user", password="csv", host="127.0.0.1", port="5432")
    create_schema(sql, con)
    insert_data(csvw, con)
    con.close()


def create_schema(sql,con):
    cur = con.cursor()
    cur.execute(sql)
    con.commit()

def insert_data(csvw,con):

    for i in range(csvw["tables"]):
        tablename = re.sub(".csv", "", csvw["tables"][i]["url"].split("/")[-1])
        insert = "COPY "+tablename+" FROM "+ csvw["tables"][i]["url"] + " CSV HEADER;"
        cur = con.cursor
        cur.execute(insert)
        con.commit()

