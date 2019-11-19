
from selection.readRMLTriplesMap import mapping_parser
from selection.yarrrml2rml import yarrrml2rml
from selection.selectMappingFromSPARQL import fromSPARQLtoMapping
import argparse
import sys


def main():
    print("Inserting headers in CSV files")

    print("Removing FnO functions from RML")
    functions, mapping = yarrrml2rml("./tmp/mapping.yml")

    print("Selecting RML rules for answering the query")
    # this function creates the rml rules needed to answer query from yarrrml mapping
    fromSPARQLtoMapping(mapping, "query")

    print("Selecting CSV files for answering the query")
    # get the triplesMaps objects from RML
    triples_map_list = mapping_parser("./tmp/mapping.rml.ttl")
    # obtain the CSV and columns based on mapping
    # ToDo: Freddy here insert your functions

    print("Cleaning CSV files based on CSVW")
    # cleaning stuff

    print("Normalizing CSV files")
    # normalize

    print("Creating new columns based on FnO functions on RML")

    print("Removing duplicates")

    print("Answering query")

if __name__ == "__main__":
    main()
