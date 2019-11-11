import os

class CSVFile:
    def __init__(self, path, delimiter):
        self.path = path
        self.delimiter = delimiter
        self.dict = self.build_csv_dictionary()

    def build_csv_dictionary(self):
        csv_dict = {
            "Id": "1",
            "Name": "2",
            "Status": "3",
            "Webpage": "4",
            "Phone": "5",
            "Email": "6",
            "Suffix": "7",
            "Birthdate": "8",
        }
        return csv_dict


class CutCommandsGenerator:
    def __init__(self, rml_path, csv_file):
        self.rml_url = rml_path
        self.csv_file = csv_file

    def generate_cut_command(self, sparql_path):
        field_numbers = self.get_correspond_columns_number(sparql_path)
        result = 'cut -d ' + self.csv_file.delimiter + ' -f ' + str(field_numbers) + ' ' + self.csv_file.path
        return result

    def get_correspond_columns_number(self, sparql_path):
        correspond_column_name = self.get_correspond_columns_name(sparql_path)
        return self.csv_file.dict[correspond_column_name]

    def get_correspond_columns_name(self, sparql_path):
        return 'Id'


student_csv = CSVFile("examples/studentsport/STUDENT.csv", ",")
p1 = CutCommandsGenerator("examples/studentsport/example1-mapping-csv.ttl", student_csv)

print(p1.rml_url)
print(p1.csv_file.path)
cut_command = p1.generate_cut_command('sparql_url')
print(cut_command)
os.system(cut_command)
