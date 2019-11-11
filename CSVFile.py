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
