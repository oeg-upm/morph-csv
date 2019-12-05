import argparse
import sys
import json

from selection.resourcesFromSparql import *
from selection.yarrrml import *
from utils.utilsresources import *
from clean import csvFormatter  as formatter
from clean import csvwParser as csvwParser
from formalization import formalization as formalizer
import schema_generation.from_mapping_to_sql as mapping2Sql
import schema_generation.create_and_insert as insert
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--json_config", required=True, help="Input config file with yarrrml and csvw")
    parser.add_argument("-q", "--sparql_query", required=True, help="SPARQL query")
    args = parser.parse_args()
    if len(sys.argv) == 5:
        try:
            with open(args.json_config, "r") as json_file:
                config = json.load(json_file)
            query = str(args.sparql_query)
            sparqlQueryParser(query)
            parsedQuery = json.loads(open('tmp/annotations/sparql.json').read())
            print(parsedQuery)
        except ValueError:
            print("No input the correct arguments, run pip3 morphcsv.py -h to see the help")
            sys.exit()
    else:
        print("No input the correct arguments, run pip3 morphcsv.py -h to see the help)")
        sys.exit()

    print("Downloading mappings, data and query")
    maketmpdirs()
    downloadAnnotations(config)
    downloadCSVfilesFromRML()
    query = readQuery(query)
    print("Removing FnO functions from RML")
    functions, mapping = getCleanYarrrml()
    print('*******************************************************')
    print(functions)
    print('*******************************************************')
    print("Selecting RML rules, CSV files and columns for answering the query")
    # this function creates the rml rules needed to answer query from yarrrml mapping
    #all_columns = [{"source": "person", "columns": ["name","ln2","ln1"]}]
    csvColumns, mapping = fromSPARQLtoMapping(mapping, query, parsedQuery) 
    print('FUCNTIONS:\n\n\n' + str(functions).replace('\'', '"'))
    #TODO ESTE CODIGO NO FUNCIONA BIEN csvColumns = getColumnsFromFunctions(csvColumns, functions)
    print("Required Columns: "+ str(csvColumns))
    csvw = csvwParser.jsonLoader('./tmp/annotations/annotations.json')
    csvw = formatter.csvwFilter(csvw,csvColumns)
    csvw = csvwParser.insertRowTitles(csvw)
    print('CSVw:\n' + str(csvw).replace('\'', '"'))
    print("CSVW filtered")
    formalizedData = formalizer.addNormalizedTablesToCsvw(csvw, mapping, query, parsedQuery)
    csvw = formalizedData['csvw']
    query = formalizedData['query']
    mapping = formalizedData['mapping']
    print('QUERY:\n' + str(query))
    formalizer.toThirdNormalForm(mapping, csvColumns, csvw)
    sys.exit()
    print("Data Normalized")
    # create the full cleaning and selection bash script
    # cleaning stuff
    #print("FilterColumns: " +  str(csvColumns))
    #csvColumns ={'routes': {'source': 'ROUTES.csv', 'columns': ['route_url','agency_id', 'route_id']}, 'agency': {'source': 'AGENCY.csv', 'columns': ['agency_url', 'agency_name', 'agency_id']}}
    formatter.csvFormatter(csvw)
    print("Data Formatted")
    schema = mapping2Sql.generate_sql_schema(csvw)
    insert.create_and_insert(csvw, schema)
    mapping2Sql.generate_sql_schema(csvw)
    #csvColumns ={'routes': {'source': 'ROUTES.csv', 'columns': ['route_url','agency_id', 'route_id']}, 'agency': {'source': 'AGENCY.csv', 'columns': ['agency_url', 'agency_name', 'agency_id']}}
    #csvFormatter(csvw)
    print("Normalizing CSV files")
    # normalize

    print("Creating new columns based on FnO functions on RML")

    print("Removing duplicates")

    print("Translating YARRRML to R2RML...")
    #TODO  fromSourceToTables is void
    #mapping = fromSourceToTables(mapping)

    print("Answering query")


if __name__ == "__main__":
    main()
