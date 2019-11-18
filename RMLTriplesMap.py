from RMLTermMap import RMLTermMap
from RMLTermMap import TermMapType
from RMLPredicateObjectMap import RMLPredicateObjectMap
from RMLLogicalSource import RMLLogicalSource
from CSVFile import CSVFile


class RMLTriplesMap:
    def __init__(self, logical_source, subject_map, predicate_object_maps):
        self.logical_source = logical_source
        self.subject_map = subject_map
        self.predicate_object_maps = predicate_object_maps


def build_example_triples_map_student():
    student_csv = CSVFile("examples/studentsport/STUDENT.csv", ",")
    logical_source = RMLLogicalSource(student_csv, "", "")
    subject_map = RMLTermMap(TermMapType.TEMPLATE_MAP, "http://example.org/Student/{Id}")
    predicate_map = RMLTermMap(TermMapType.CONSTANT_MAP, "http://example.org/hasStudentName")
    object_map = RMLTermMap(TermMapType.COLUMN_MAP, "Name")
    predicate_object_map = RMLPredicateObjectMap(predicate_map, object_map)
    predicate_object_maps = [predicate_object_map]
    example_triples_map = RMLTriplesMap(logical_source, subject_map, predicate_object_maps)
    return example_triples_map


def build_example_triples_map_sport():
    sport_csv = CSVFile("examples/studentsport/SPORT.csv", ",")
    logical_source = RMLLogicalSource(sport_csv, "", "")
    subject_map = RMLTermMap(TermMapType.TEMPLATE_MAP, "http://example.org/Sport/{ID}")
    predicate_map = RMLTermMap(TermMapType.CONSTANT_MAP, "http://example.org/hasSportName")
    object_map = RMLTermMap(TermMapType.COLUMN_MAP, "Name")
    predicate_object_map = RMLPredicateObjectMap(predicate_map, object_map)
    predicate_object_maps = [predicate_object_map]
    example_triples_map = RMLTriplesMap(logical_source, subject_map, predicate_object_maps)
    return example_triples_map
