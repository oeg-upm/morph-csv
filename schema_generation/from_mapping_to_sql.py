import re


# return true if there is a join in the mapping, hence, in the query, if not morph-rdb in csv mode should be run
def decide_schema_based_on_query(mapping):
    for tm in mapping["mappings"]:
        for pom in mapping["mappings"]["po"]:
            # if p in pom means there is a join in the mapping
            if 'p' in pom:
                return True
    return False


def generate_sql_schema(csvw):
    sql = ""
    foreignkeys = ""
    for i in range(csvw["tables"]):
        source = re.sub(".csv", "", csvw["tables"][i]["url"].split("/")[-1])
        columns = csvw["tables"][i]["tableSchema"]["filteredRowTitles"]

        sql += "DROP TABLE " + source + ";\n"
        sql += "CREATE TABLE " + source + "("

        for j in range(len(columns)):
            sql += columns[i] + " " + find_type_in_csvw(columns[j], csvw["tables"][i]["tableSchema"]) + ",\n"

        primarykeys = csvw["tables"][i]["tableSchema"]["primaryKey"]
        if not re.match("", primarykeys):
            sql += "PRIMARY KEY (" + primarykeys + "),\n"

        for fk in range(csvw["tables"][i]["tableSchema"]["foreignKeys"]):
            column = csvw["tables"][i]["tableSchema"]["foreignKeys"][fk]["columnReference"]
            table = csvw["tables"][i]["tableSchema"]["foreignKeys"][fk]["reference"]["resource"]
            reference = csvw["tables"][i]["tableSchema"]["foreignKeys"][fk]["reference"]["columnReference"]
            foreignkeys += "FOREIGN KEY ("+column+") REFERENCES "+table+" ("+reference+"),\n"
        sql += foreignkeys
        sql += sql[-1] + ");\n"


def find_type_in_csvw(title, csvw_columns):
    datatype = "VARCHAR(200)"
    for i in range(csvw_columns["columns"]):
        if csvw_columns["columns"][i]["titles"][0] == title:
            datatype = translate_type_to_sql(csvw_columns["columns"][i]["datatype"])
    return datatype


def translate_type_to_sql(type):
    if re.match("integer", type):
        translated_type = "INT"
    elif re.match("boolean", type):
        translated_type = "BOOLEAN"
    elif re.match("decimal", type):
        translated_type = "DECIMAL(18,15)"
    else:
        translated_type = "VARCHAR(200)"

    return translated_type
