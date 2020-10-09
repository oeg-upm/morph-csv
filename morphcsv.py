import argparse
import sys
import json
import time

from selection.resourcesFromSparql import *
from selection.yarrrml import *
from utils.utilsresources import *
from clean import csvFormatter as formatter
from clean import csvwParser as csvwParser
from normalization import normalization as normalizer
import schema_generation.from_mapping_to_sql as mapping2Sql
import schema_generation.create_and_insert as insert
import schema_generation.creation_sql_alters as sqlAlters
import schema_generation.morph_properties as genproperties

def main():
    measuredTimes = {'selection':0,'normalization':0,'dataPreparation':0,'schemaCreationAndLoad':0}
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--json_config", required=True, help="Input config file with yarrrml and csvw")
    parser.add_argument("-q", "--sparql_query", required=False, help="SPARQL query")
    parser.add_argument("-n", "--naive", required=False, help="Morph-csv Naive mode")

    args = parser.parse_args()
    if len(sys.argv) == 5:
        try:
            with open(args.json_config, "r") as json_file:
                config = json.load(json_file)
            query_path = str(args.sparql_query)

        except ValueError:
            print("No input the correct arguments, run pip3 morphcsv.py -h to see the help")
            sys.exit()
    else:
        print("No input the correct arguments, run pip3 morphcsv.py -h to see the help)")
        sys.exit()
    print("Downloading mappings, data and query")
    maketmpdirs()
    downloadAnnotations(config)
    #downloadCSVfilesFromRML()
    query = readQuery(query_path)
    sparqlQueryParser(query_path)
    parsedQuery = json.loads(open('tmp/annotations/sparql.json').read())    
    print("Removing FnO functions from RML")
    functions, mapping = getCleanYarrrml()
    #-----------------------------------SELECTION-------------------
    print("Selecting RML rules, CSVW annotations and CSV files and columns for answering the query")
    selectionTime = time.time()
    csvColumns, mapping = fromSPARQLtoMapping(mapping, query, parsedQuery)
    csvColumns,functions = getColumnsFromFunctions(csvColumns, functions)
    #print('Required Columns: '+ str(csvColumns).replace("'", "\""))
    csvw = csvwParser.jsonLoader('./tmp/annotations/annotations.json')
    csvw = csvwParser.insertRowTitles(csvw)
    csvw = formatter.csvwFilter(csvw,csvColumns)
    measuredTimes['selection'] = time.time() - selectionTime
    #--------------------------END SELECTION--------------------------------------------------

    print("Formalizing the data to 2NF")
    #-----------------------NORMALIZATION------------------------------------------------
    normalizationTime = time.time()
    formalizedData = normalizer.addNormalizedTablesToCsvw(csvw, mapping, query, parsedQuery)
    measuredTimes['normalization'] = time.time() - normalizationTime
    #-----------------------END NORMALIZATION------------------------------------------------

    csvw = formalizedData['csvw']
    query = formalizedData['query']
    mapping = formalizedData['mapping']
    print("Preparing the data to execute the query")

    #--------------------DATA PREPARATION--------------------
    dataPreparationTime = time.time()
    formatter.csvFormatter(csvw)
    measuredTimes['dataPreparation'] = time.time() - dataPreparationTime
    #---------------------END DATA PREPARATION---------------

    print("Tanslating the RML mapping without functions to R2RML")
    #----------------MAPPING TRANSLATION---------------------
    mappingTranslationTime = time.time()
    fromSourceToTables(mapping)#Medir
    measuredTimes['mappingTranslation'] = time.time() - mappingTranslationTime
    #----------------END MAPPING TRANSLATION---------------------

    print("Generating the SQL schema based on the csvw and the query")
    #----------------------SCHEMA CREATION AND LOAD-----------------------------------
    schemaCreationAndLoadTime = time.time()
    schema, alters = mapping2Sql.generate_sql_schema(csvw,mapping,mapping2Sql.decide_schema_based_on_query(mapping))
    insert.create_and_insert(csvw, schema, sqlAlters.translate_fno_to_sql(functions), alters)
    measuredTimes['schemaCreationAndLoad'] = time.time() - schemaCreationAndLoadTime
    print(str(schema).replace(';',';\n\n').replace(',',',\n'))
    #----------------------END SCHEMA CREATION AND LOAD-----------------------------------
    print("Execution Times: ")
    print(json.dumps(measuredTimes, indent=2))
    print("Answering query")

if __name__ == "__main__":
    main()
