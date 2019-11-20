
from selection.readRMLTriplesMap import mapping_parser
from selection.yarrrml2rml import yarrrml2rml
from selection.resorucesFromSPARQL import fromSPARQLtoMapping, getColumnsFromFunctions
import argparse
import sys
import json


def main():
    print("Removing FnO functions from RML")
    functions, mapping = yarrrml2rml("./tmp/mapping.yml")
    print("Selecting RML rules, CSV files and columns for answering the query")
    # this function creates the rml rules needed to answer query from yarrrml mapping
    csvColumns = getColumnsFromFunctions(fromSPARQLtoMapping(mapping, "query"), functions)
    print(csvColumns)
    print("Cleaning CSV files based on CSVW")
    # cleaning stuff

    print("Normalizing CSV files")
    # normalize

    print("Creating new columns based on FnO functions on RML")

    print("Removing duplicates")

    print("Answering query")

if __name__ == "__main__":
    main()
