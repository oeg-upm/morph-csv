
from yarrrml2rml import *
from read import *

if __name__ == "__main__":
    functions = yarrrml2rml("./examples/mapping.yml")
    triples_map_list = mapping_parser("./examples/mapping.rml.ttl")
    print(triples_map_list)