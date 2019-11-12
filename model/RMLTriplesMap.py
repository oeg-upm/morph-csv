from model.RMLTermMap import RMLTermMap
from model.RMLTermMap import TermMapType
from model.RMLPredicateObjectMap import RMLPredicateObjectMap
from model.RMLLogicalSource import RMLLogicalSource

class RMLTriplesMap:
    def __init__(self, logical_source, subject_map, predicate_object_maps):
        self.logical_source = logical_source
        self.subject_map = subject_map
        self.predicate_object_maps = predicate_object_maps


def build_example_triples_map():
        subject_map = RMLTermMap(TermMapType.TEMPLATE_MAP, "http://example.org/{Id}")
        predicate_map = RMLTermMap(TermMapType.CONSTANT_MAP, "http://example.org/hasName")
        object_map = RMLTermMap(TermMapType.COLUMN_MAP, "Name")
        predicate_object_map = RMLPredicateObjectMap(predicate_map, object_map)
        logical_source = RMLLogicalSource("tmp/studentsport/STUDENT.csv", "", "")

        example_triples_map = RMLTriplesMap(logical_source, subject_map, [predicate_object_map])
        return example_triples_map

