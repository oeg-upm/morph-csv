import re
import sys
import clean.csvwParser as csvwParser
import schema_generation.creation_sql_alters as function


# return true if there is a join in the mapping, hence, in the query, if not morph-rdb in csv mode should be run

def decide_schema_based_on_query(mapping):
    for tm in mapping["mappings"]:
        for pom in mapping["mappings"][tm]["po"]:
            # if p in pom means there is a join in the mapping
            if 'p' in pom:
                return True
    return False


def generate_sql_schema(csvw,functions,decision):

    sqlGlobal = ""
    foreignkeys = ""
    for i,table in enumerate(csvw["tables"]):
        sql = ''
        source = csvwParser.getUrl(table).split("/")[-1:][0].replace(".csv","")
        columns = csvw["tables"][i]["filteredRowTitles"]
        sql += "DROP TABLE IF EXISTS \"" + source + "\";"
        sql += "CREATE TABLE \"" + source + "\"("
        for columName in columns:
            sql += columName + " " + find_type_in_csvw(columName, table["tableSchema"]) + ","

        if decision:
            try:
                primarykeys = table["tableSchema"]["primaryKey"]
            except:
                primarykeys = ''
            if len(primarykeys) > 0:
                sql += "PRIMARY KEY (" + primarykeys + "),"
            if 'foreignKeys' in table['tableSchema'].keys():
                for fk in table["tableSchema"]["foreignKeys"]:
                    column = fk["columnReference"]
                    table = fk["reference"]["resource"]
                    reference = fk["reference"]["columnReference"]
                    foreignkeys += "FOREIGN KEY ("+column+") REFERENCES "+table+" ("+reference+"),"
                sql += foreignkeys

        sql = sql[:-1] + ");"
        sqlGlobal += sql
    sqlGlobal += function.translate_fno_to_sql(functions)
    #print('***********FUNCTIIONS**********')
    #print(str(functions).replace('\'','"'))
    print('***********SCHEMA**************')
    print(sqlGlobal.replace(';', ';\n'))
    return sqlGlobal

def find_type_in_csvw(title, csvw_columns):
    datatype = "VARCHAR(200)"
    for col in csvw_columns["columns"]:
        if csvwParser.getColTitle(col) == title:
            datatype = translate_type_to_sql(csvwParser.getDataTypeValue(col))
    return datatype

def translate_type_to_sql(dataType):
    if re.match("integer", dataType):
        translated_type = "INT"
    elif re.match("boolean", dataType):
        translated_type = "BOOLEAN"
    elif re.match("decimal", dataType):
        translated_type = "DECIMAL(40,15)"
    elif re.match("date", dataType):
        translated_type = "DATE"
    else:
        translated_type = "VARCHAR(500)"

    return translated_type
