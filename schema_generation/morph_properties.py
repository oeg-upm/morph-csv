
import re


"""
mappingdocument.file.path=example1-mapping-csv.ttl
output.file.path=example1-batch-result-csv.nt

output.rdflanguage=N-TRIPLE

csv.file.path = SPORT.csv, STUDENT.csv
no_of_database=1
database.name[0]=morphcsv
database.driver[0]=org.h2.Driver
database.url[0]=jdbc:h2:mem:morphcsv
database.user[0]=sa
database.pwd[0]=
database.type[0]=CSV
"""

def csv_basic_generation(mapping,query_path):
    properties = ""
    sources = []
    for tm in mapping["mappings"]:
        source = re.sub("~csv", "", (mapping["mappings"][tm]["sources"][0][0].split("/")[-1]))
        sources.extend("tmp/csv/"+source+".csv")

    properties += "mappingdocument.file.path=/morphcsv/tmp/annotations/mapping.r2rml.ttl\n"
    properties += "output.file.path=/results/results.xml\n"
    properties += "query.file.path="+query_path
    properties += "csv.file.path="
    for i in range(len(sources)):
        if i < (len(sources)-1):
            properties += sources[i]+","
        else:
            properties += sources[i]+"\n"
    properties += "no_of_database=1\n"
    properties += "database.name[0]=morphcsv\n"
    properties += "database.driver[0]=org.h2.Driver\n"
    properties += "database.url[0]=jdbc:h2:mem:morphcsv\n"
    properties += "database.user[0]=sa\n"
    properties += "database.pwd[0]=\n"
    properties += "database.type[0]=CSV\n"

    f = open("tmp/morph-properties/morph-rdb.properties", "w+")
    f.write(properties)
    f.close()

def postgre_generation(query_path):
    properties = ""
    properties += "mappingdocument.file.path=/morphcsv/tmp/annotations/mapping.r2rml.ttl\n"
    properties += "output.file.path=/results/results.xml\n"
    properties += "query.file.path=" + query_path
    properties += "no_of_database=1\n"
    properties += "database.name[0]=morphcsv\n"
    properties += "database.driver[0]=org.postgresql.Driver\n"
    properties += "database.url[0]=jdbc:postgresql://postgres/morphcsv\n"
    properties += "database.user[0]=user\n"
    properties += "database.pwd[0]=csv\n"
    properties += "database.type[0]=postgresql\n"

    f = open("tmp/morph-rdb.properties", "w+")
    f.write(properties)
    f.close()


