import argparse
import sys
import json

from selection.resourcesFromSparql import *
from selection.yarrrml import *
from utils.utilsresources import *
from clean import csvFormatter as formatter
from clean import csvwParser as csvwParser
from formalization import formalization as formalizer
import schema_generation.from_mapping_to_sql as mapping2Sql
import schema_generation.create_and_insert as insert
import schema_generation.morph_properties as genproperties

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--json_config", required=True, help="Input config file with yarrrml and csvw")
    parser.add_argument("-q", "--sparql_query", required=True, help="SPARQL query")
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
#    downloadAnnotations(config)
#   downloadCSVfilesFromRML()

    query = readQuery(query_path)
    sparqlQueryParser(query_path)
    parsedQuery = json.loads(open('tmp/annotations/sparql.json').read())

    print("Removing FnO functions from RML")
    functions, mapping = getCleanYarrrml()
    print("Selecting RML rules, CSVW annotations and CSV files and columns for answering the query")
    csvColumns, mapping = fromSPARQLtoMapping(mapping, query, parsedQuery) 
    csvColumns,functions = getColumnsFromFunctions(csvColumns, functions)
    #functions = filterFunctionsAccording2Query(functions, mapping)
    print('Required Columns: '+ str(csvColumns).replace("'", "\""))
    csvw = csvwParser.jsonLoader('./tmp/annotations/annotations.json')
    csvw = csvwParser.insertRowTitles(csvw)
#    print('++++++++++++++++CSVW++++++++++++++++')
#    print(str(csvw).replace('\'','"').replace('True', 'true').replace('False', 'false'))
    csvw = formatter.csvwFilter(csvw,csvColumns)
    #print('***********CSVW************')
    #print(csvw)
    print("Formalizing the data to 2NF")
    formalizedData = formalizer.addNormalizedTablesToCsvw(csvw, mapping, query, parsedQuery)
    csvw = formalizedData['csvw']
    query = formalizedData['query']
    mapping = formalizedData['mapping']
    #TODO formalizer.toThirdNormalForm(mapping, csvColumns, csvw)
    print("Preparing the data to execute the query")
    formatter.csvFormatter(csvw)
    print("Tanslating the RML mapping without functions to R2RML")
    fromSourceToTables(mapping)
    print("Generating the SQL schema based on the csvw and the query")
    schema = mapping2Sql.generate_sql_schema(csvw,functions,mapping2Sql.decide_schema_based_on_query(mapping))
    print(str(schema).replace(';',';\n'))
    insert.create_and_insert(csvw, schema)
    print("Answering query")

if __name__ == "__main__":
    main()
