

from selection.readRMLTriplesMap import mapping_parser
from selection.yarrrml2rml import yarrrml2rml
import sys

if __name__ == "__main__":

    #remove functions and translate yarrrml to rml
    functions = yarrrml2rml("./tmp/mapping.yml")
    #get the triplesMaps objects from RML
    triples_map_list = mapping_parser("./tmp/mapping.rml.ttl")
    #obtain the triplesMap based on a query
