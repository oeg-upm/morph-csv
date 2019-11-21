import argparse
import sys
import json
from utils.utilsresources import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--json_config", required=True, help="Input config file with yarrrml and csvw")
    parser.add_argument("-q", "--sparql_query", required=True, help="SPARQL query")
    args = parser.parse_args()
    print(sys.argv)
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
    downloadAnnotations(config)
    downloadCSVfilesFromRML(config["yarrrml"])
    query = readQuery(query)
    print("Removing FnO functions from RML")
    #functions, mapping = yarrrml2rml("./tmp/mapping.yml")
    print("Selecting RML rules, CSV files and columns for answering the query")
    # this function creates the rml rules needed to answer query from yarrrml mapping
    #csvColumns = getColumnsFromFunctions(fromSPARQLtoMapping(mapping, query), functions)
    print("Cleaning CSV files based on CSVW")
    # cleaning stuff

    print("Normalizing CSV files")
    # normalize

    print("Creating new columns based on FnO functions on RML")

    print("Removing duplicates")

    print("Answering query")

if __name__ == "__main__":
    main()
