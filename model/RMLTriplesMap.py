from model.CSVFile import CSVFile
from model.RMLTermMap import RMLTermMap
from model.RMLTermMap import TermMapType
from model.RMLPredicateObjectMap import RMLPredicateObjectMap
from model.RMLLogicalSource import RMLLogicalSource
from model.RMLJoinCondition import RMLJoinCondition
from model.RMLRefObjectMap import RMLRefObjectMap


class RMLTriplesMap:
    def __init__(self, logical_source, subject_map, predicate_object_maps):
        self.logical_source = logical_source
        self.subject_map = subject_map
        self.predicate_object_maps = predicate_object_maps


def build_example_triples_map_student():
    student_csv = CSVFile("../tmp/studentsport/STUDENT.csv", ",")
    logical_source = RMLLogicalSource(student_csv, "", "")
    subject_map = RMLTermMap(TermMapType.TEMPLATE_MAP, "http://example.org/Student/{Id}")

    predicate_map1 = RMLTermMap(TermMapType.CONSTANT_MAP, "http://example.org/hasStudentName")
    object_map1 = RMLTermMap(TermMapType.COLUMN_MAP, "Name")
    predicate_object_map1 = RMLPredicateObjectMap(predicate_map1, object_map1)

    predicate_map2 = RMLTermMap(TermMapType.CONSTANT_MAP, "http://example.org/plays")
    join_condition = RMLJoinCondition("Sport", "ID")
    object_map2 = RMLRefObjectMap("TMSport", join_condition)
    predicate_object_map2 = RMLPredicateObjectMap(predicate_map2, object_map2)

    predicate_object_maps = [predicate_object_map1, predicate_object_map2]
    example_triples_map = RMLTriplesMap(logical_source, subject_map, predicate_object_maps)
    return example_triples_map


def build_example_triples_map_sport():
    sport_csv = CSVFile("../tmp/studentsport/SPORT.csv", ",")
    logical_source = RMLLogicalSource(sport_csv, "", "")
    subject_map = RMLTermMap(TermMapType.TEMPLATE_MAP, "http://example.org/Sport/{Id}")
    predicate_map = RMLTermMap(TermMapType.CONSTANT_MAP, "http://example.org/hasSportName")
    object_map = RMLTermMap(TermMapType.COLUMN_MAP, "Name")
    predicate_object_map = RMLPredicateObjectMap(predicate_map, object_map)
    predicate_object_maps = [predicate_object_map]
    example_triples_map = RMLTriplesMap(logical_source, subject_map, predicate_object_maps)
    return example_triples_map
