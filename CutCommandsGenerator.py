import os

from CSVFile import CSVFile
from RMLTriplesMap import RMLTriplesMap
from RMLTriplesMap import build_example_triples_map
from RMLTermMap import string_separetion

class CutCommandsGenerator:
    def __init__(self, rml_path, csv_file):
        self.rml_url = rml_path
        self.csv_file = csv_file

    def get_column_number(self, column_name):
        column_number = self.csv_file.dict[column_name]
        return column_number

    def generate_cut_command(self, sparql_path):
        field_numbers = self.get_correspond_columns_numbers(sparql_path)
        joined_field_numbers = ','.join(field_numbers)
        result = 'cut -d ' + self.csv_file.delimiter + ' -f ' + joined_field_numbers + ' ' + self.csv_file.path
        return result

    def get_correspond_columns_numbers(self, sparql_path):
        correspond_columns_names = self.get_correspond_columns_names(sparql_path)
        correspond_columns_numbers = list(map(self.get_column_number, correspond_columns_names))
        return correspond_columns_numbers

    def get_correspond_columns_names(self, sparql_path):
        correspond_triples_map = self.get_correspond_triples_map(sparql_path)
        correspond_columns_names = self.get_correspond_column_name_from_triples_map(sparql_path, correspond_triples_map)
        return correspond_columns_names

    def get_correspond_triples_map(self, sparql_path):
        correspond_triples_map = build_example_triples_map()
        print(correspond_triples_map)
        return correspond_triples_map

    def get_correspond_column_name_from_triples_map(self, sparql_path, triples_map):
        subject_map = triples_map.subject_map
        correspond_columns_names_from_subject_map = self.get_correspond_columns_names_from_subject_map(sparql_path, subject_map)
        correspond_column_name_from_predicate_object_maps = self.get_correspond_columns_names_from_predicate_object_maps(sparql_path)
        correspond_columns_names = correspond_columns_names_from_subject_map + correspond_column_name_from_predicate_object_maps
        return correspond_columns_names

    def get_correspond_columns_names_from_subject_map(self, sparql_path, subject_map):
        return self.get_correspond_columns_names_from_term_map(sparql_path, subject_map)

    def get_correspond_columns_names_from_predicate_object_maps(self, sparql_path):
        return ['Name', 'Email']

    def get_correspond_columns_names_from_term_map(self, sparql_path, term_map):
        term_map_value = term_map.term_map_value
        print("term_map_value = " + term_map_value)
        reference, condition = string_separetion(term_map_value)
        print("term map condition = " + str(condition))

        return [condition]

student_csv = CSVFile("examples/studentsport/STUDENT.csv", ",")
cut_command_generator = CutCommandsGenerator("examples/studentsport/example1-mapping-csv.ttl", student_csv)
#print(cut_command_generator.rml_url)
#print(cut_command_generator.csv_file.path)
cut_command = cut_command_generator.generate_cut_command('sparql_url')
print("cut_command = " + cut_command)
os.system(cut_command)
