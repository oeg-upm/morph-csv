import os

from model.RMLTriplesMap import RMLTriplesMap
from model.RMLTriplesMap import build_example_triples_map_student
from model.RMLTriplesMap import build_example_triples_map_sport
from model.CSVFile import CSVFile
from model.RMLTermMap import string_separetion
from model.RMLTermMap import TermMapType

class CutCommandsGenerator:
    def __init__(self, rml_path, csv_files):
        self.rml_url = rml_path
        self.csv_files = csv_files

    @staticmethod
    def get_column_number(csv_file, column_name):
        column_number = csv_file.dict[column_name]
        return column_number

    @staticmethod
    def get_columns_numbers(csv_file, columns_names):
        columns_numbers = []
        for column_name in columns_names:
            column_number = CutCommandsGenerator.get_column_number(csv_file, column_name)
            columns_numbers = columns_numbers + [column_number]
        return columns_numbers

    def generate_cut_command_from_sparql(self, sparql_path):
        correspond_triples_maps = self.get_correspond_triples_maps(sparql_path)
        for triples_map in correspond_triples_maps:
            cut_command = self.generate_cut_command_from_triples_map(sparql_path, triples_map)
            print("cut_command = " + cut_command)
            os.system(cut_command)
        return 'None'

    def generate_cut_command_from_triples_map(self, sparql_path, triples_map):
        correspond_csv_file = triples_map.logical_source.source
        correspond_columns_names = self.get_correspond_columns_names_from_triples_map(sparql_path, triples_map)
        field_numbers = CutCommandsGenerator.get_columns_numbers(correspond_csv_file, correspond_columns_names)
        joined_field_numbers = ','.join(field_numbers)
        result = 'cut -d ' + correspond_csv_file.delimiter + ' -f ' + joined_field_numbers + ' ' + correspond_csv_file.path
        return result

    def get_correspond_triples_maps(self, sparql_path):
        correspond_triples_map_student = build_example_triples_map_student()
        correspond_triples_map_sport = build_example_triples_map_sport()

        correspond_triples_maps = [correspond_triples_map_student, correspond_triples_map_sport]
        return correspond_triples_maps

    def get_correspond_columns_names_from_triples_map(self, sparql_path, triples_map):
        subject_map = triples_map.subject_map
        predicate_object_maps = triples_map.predicate_object_maps

        correspond_columns_names_from_subject_map = self.get_correspond_columns_names_from_subject_map(sparql_path, subject_map)
        correspond_column_name_from_predicate_object_maps = self.get_correspond_columns_names_from_predicate_object_maps(sparql_path, predicate_object_maps)
        correspond_columns_names = correspond_columns_names_from_subject_map + correspond_column_name_from_predicate_object_maps
        return correspond_columns_names

    def get_correspond_columns_names_from_subject_map(self, sparql_path, subject_map):
        return self.get_correspond_columns_names_from_term_map(sparql_path, subject_map)

    def get_correspond_columns_names_from_predicate_object_maps(self, sparql_path, predicate_object_maps):
        object_conditions = []
        for predicate_object_map in predicate_object_maps:
            object_map = predicate_object_map.object_map
            object_condition = self.get_correspond_columns_names_from_term_map(sparql_path, object_map)
            object_conditions = object_conditions + object_condition
        return object_conditions

    def get_correspond_columns_names_from_term_map(self, sparql_path, term_map):
        term_map_value = term_map.term_map_value
        print("term_map_value = " + term_map_value)

        term_map_type = term_map.term_map_type
        print("term_map_type = " + str(term_map_type))

        correspond_columns_names = {}
        if term_map_type == TermMapType.TEMPLATE_MAP:
            reference, condition = string_separetion(term_map_value)
            correspond_columns_names = [condition]
        elif term_map_type == TermMapType.COLUMN_MAP:
            term_map_value
            correspond_columns_names = [term_map_value]

        print("correspond_columns_names = " + str(correspond_columns_names))
        return correspond_columns_names


student_csv = CSVFile("../tmp/studentsport/STUDENT.csv", ",")
sport_csv = CSVFile("../tmp/studentsport/SPORT.csv", ",")
csv_files = [student_csv, sport_csv]
cut_command_generator = CutCommandsGenerator("../tmp/studentsport/example1-mapping-csv.ttl", csv_files)

#print(cut_command_generator.rml_url)
#print(cut_command_generator.csv_file.path)
cut_command_generator.generate_cut_command_from_sparql('sparql_url')
