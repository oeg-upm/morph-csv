import argparse
import sys
import json

from selection.resorucesFromSPARQL import *
from selection.yarrrml import *
from utils.utilsresources import *
from clean.csvFormatter import *
import clean.csvwParser as csvwParser
import schema_generation.from_mapping_to_sql as mapping2Sql
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
        except ValueError:
            print("No input the correct arguments, run pip3 morphcsv.py -h to see the help")
            sys.exit()
    else:
        print("No input the correct arguments, run pip3 morphcsv.py -h to see the help)")
        sys.exit()

    print("Downloading mappings, data and query")
    maketmpdirs()
#    downloadAnnotations(config)
##    downloadCSVfilesFromRML()
    query = readQuery(query)
    print("Removing FnO functions from RML")
    functions, mapping = getCleanYarrrml()
    print("Selecting RML rules, CSV files and columns for answering the query")
    # this function creates the rml rules needed to answer query from yarrrml mapping
    #all_columns = [{"source": "person", "columns": ["name","ln2","ln1"]}]
    csvColumns, mapping = fromSPARQLtoMapping(mapping, query)
    csvColumns = getColumnsFromFunctions(csvColumns, functions)
    #print("Columnas requeridas"+str(csvColumns))
    print("Cleaning CSV files based on CSVW")
    # create the full cleaning and selection bash script
    # cleaning stuff
    print("FilterColumns"+str(csvColumns))
    csvw = csvwParser.jsonLoader('./tmp/annotations/annotations.json')
    #print('\n\n\nOLD CSVW\n\n\n' + str(csvw).replace('\'', '"') + '\n\n\n')
    csvw = csvwParser.insertRowTitles(csvw)
    #print('\n\n\nNEW CSVW\n\n\n' + str(csvw).replace('\'', '"').replace('True', 'true').replace('False', 'false') + '\n\n\n')
    csvw = csvwFilter(csvw,csvColumns)
    mapping2Sql.generate_sql_schema(csvw)
    #csvColumns ={'routes': {'source': 'ROUTES.csv', 'columns': ['route_url','agency_id', 'route_id']}, 'agency': {'source': 'AGENCY.csv', 'columns': ['agency_url', 'agency_name', 'agency_id']}}
    csvFormatter(csvw)
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
