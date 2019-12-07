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
    downloadCSVfilesFromRML()

    query = readQuery(query_path)
    sparqlQueryParser(query_path)
    parsedQuery = json.loads(open('tmp/annotations/sparql.json').read())

    print("Removing FnO functions from RML")
    functions, mapping = getCleanYarrrml()
    print("Selecting RML rules, CSV files and columns for answering the query")
    # this function creates the rml rules needed to answer query from yarrrml mapping
    csvColumns, mapping = fromSPARQLtoMapping(mapping, query, parsedQuery) 
    csvColumns = getColumnsFromFunctions(csvColumns, functions)
    print("Required Columns: "+ str(csvColumns))
    #sys.exit()
    csvw = csvwParser.jsonLoader('./tmp/annotations/annotations.json')
    csvw = csvwParser.insertRowTitles(csvw)
    csvw = formatter.csvwFilter(csvw,csvColumns)
    print("CSVW filtered")
    formalizedData = formalizer.addNormalizedTablesToCsvw(csvw, mapping, query, parsedQuery)
    csvw = formalizedData['csvw']
    query = formalizedData['query']
    mapping = formalizedData['mapping']
    #TODO formalizer.toThirdNormalForm(mapping, csvColumns, csvw)
    print("Data Normalized")
    formatter.csvFormatter(csvw)
    print("Data Formatted")
    schema = mapping2Sql.generate_sql_schema(csvw)
    insert.create_and_insert(csvw, schema)
    mapping2Sql.generate_sql_schema(csvw)
    #mapping = fromSourceToTables(mapping)
    print("Answering query")

if __name__ == "__main__":
    main()
