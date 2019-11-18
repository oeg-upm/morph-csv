import os

from model.RMLTriplesMap import build_example_triples_map_student
from model.RMLTriplesMap import build_example_triples_map_sport
from model.CSVFile import CSVFile
from model.RMLTermMap import string_separetion
from model.RMLTermMap import TermMapType
from model.RMLTermMap import RMLTermMap
from model.RMLRefObjectMap import RMLRefObjectMap
from model.RMLJoinCondition import RMLJoinCondition


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
        field_numbers = sorted(field_numbers)
        field_numbers = list(dict.fromkeys(field_numbers))
        print("field_numbers = " + str(field_numbers))

        field_numbers_with_dollar = ['"\\""$' + str(field_number) + '"\\","' for field_number in field_numbers[:-1]]
        field_numbers_with_dollar.append('"\\""$' + str(field_numbers[-1:][0]) + '"\\""')
        if('1' in field_numbers):
            field_numbers_with_dollar[0] = '$1"\\","'
        joined_field_numbers = ''.join(str(field_numbers))
        joined_field_numbers_with_dollar = ','.join(field_numbers_with_dollar)
        print("joined_field_numbers_with_dollar = " + str(joined_field_numbers_with_dollar))
        result_with_cut = 'cut -d ' + correspond_csv_file.delimiter + ' -f ' + ','.join(str(field_numbers)) + ' ' + correspond_csv_file.path
        result_with_awk = 'awk -F \'\\"' + correspond_csv_file.delimiter + '\\"\' \'{print ' + joined_field_numbers_with_dollar + '}\' ' + correspond_csv_file.path
        print("result_with_awk = " + str(result_with_awk))
        return result_with_awk

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
        correspond_columns_names = []
        for predicate_object_map in predicate_object_maps:
            object_map = predicate_object_map.object_map
            if isinstance(object_map, RMLTermMap):
                correspond_column = self.get_correspond_columns_names_from_term_map(sparql_path, object_map)
                correspond_columns_names = correspond_columns_names + correspond_column
            elif isinstance(object_map, RMLRefObjectMap):
                join_condition = object_map.join_condition
                correspond_column = self.get_correspond_columns_names_from_join_condition(join_condition)
                correspond_columns_names = correspond_columns_names + correspond_column

        return correspond_columns_names

    def get_correspond_columns_names_from_term_map(self, sparql_path, term_map):
        term_map_value = term_map.term_map_value
        #print("term_map_value = " + term_map_value)
        term_map_type = term_map.term_map_type
        #print("term_map_type = " + str(term_map_type))
        correspond_columns_names = {}
        if term_map_type == TermMapType.TEMPLATE_MAP:
            reference, condition = string_separetion(term_map_value)
            correspond_columns_names = [condition]
        elif term_map_type == TermMapType.COLUMN_MAP:
            term_map_value
            correspond_columns_names = [term_map_value]
        #print("correspond_columns_names = " + str(correspond_columns_names))
        return correspond_columns_names

    def get_correspond_columns_names_from_join_condition(self, join_condition:RMLJoinCondition):
        correspond_columns_names = [join_condition.child_column_name]
        #print("correspond_columns_names = " + str(correspond_columns_names))
        return correspond_columns_names

student_csv = CSVFile("../tmp/studentsport/STUDENT.csv", ",")
sport_csv = CSVFile("../tmp/studentsport/SPORT.csv", ",")
csv_files = [student_csv, sport_csv]
cut_command_generator = CutCommandsGenerator("../tmp/studentsport/example1-mapping-csv.ttl", csv_files)

#print(cut_command_generator.rml_url)
#print(cut_command_generator.csv_file.path)
cut_command_generator.generate_cut_command_from_sparql('sparql_url')
