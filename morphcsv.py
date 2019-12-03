import argparse
import sys
import json

from selection.resourcesFromSparql import *
from selection.yarrrml import *
from utils.utilsresources import *
from clean import csvFormatter  as formatter
from clean import csvwParser as csvwParser
from formalization import formalization as formalizer
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
    #downloadAnnotations(config)
    #downloadCSVfilesFromRML()
    query = readQuery(query)
    print("Removing FnO functions from RML")
    functions, mapping = getCleanYarrrml()
    print("Selecting RML rules, CSV files and columns for answering the query")
    # this function creates the rml rules needed to answer query from yarrrml mapping
    #all_columns = [{"source": "person", "columns": ["name","ln2","ln1"]}]
    csvColumns, mapping = fromSPARQLtoMapping(mapping, query, parsedQuery) 
    print('\n\n\n**************OLD CSV COLUMNS***************\n\n\n')
    print(csvColumns)
    print('\n\n\n')
    csvColumns = getColumnsFromFunctions(csvColumns, functions)
    print("Required Columns: "+ str(csvColumns))
    sys.exit()
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
    formalizer.toThirdNormalForm(mapping)
    sys.exit()
    print("Data Normalized")
    # create the full cleaning and selection bash script
    # cleaning stuff
    #print("FilterColumns"+str(csvColumns))
    #csvColumns ={'routes': {'source': 'ROUTES.csv', 'columns': ['route_url','agency_id', 'route_id']}, 'agency': {'source': 'AGENCY.csv', 'columns': ['agency_url', 'agency_name', 'agency_id']}}
    formatter.csvFormatter(csvw)
    print("Data Formatted")

    # normalize

    print("Creating new columns based on FnO functions on RML")

    print("Removing duplicates")

    print("Translating YARRRML to R2RML...")
    #TODO  fromSourceToTables is void
    #mapping = fromSourceToTables(mapping)

    print("Answering query")


if __name__ == "__main__":
    main()
