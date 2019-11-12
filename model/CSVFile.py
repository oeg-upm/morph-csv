import pandas as pd


class CSVFile:
    def __init__(self, path, delimiter):
        self.path = path
        self.delimiter = delimiter
        self.dict = self.build_csv_dictionary()


    def build_csv_dictionary(self):
        csv_columns = pd.read_csv(self.path).columns
        csv_dict = {}
        i = 1
        for column_name in csv_columns:
            csv_dict[column_name] = str(i)
            i = i + 1
        print('csv_dict = ' + str(csv_dict))

        return csv_dict
