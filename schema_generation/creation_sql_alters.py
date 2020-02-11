
import re

def translate_fno_to_sql(functions):
    sql = ""
    for tm in functions:
        #if 'query' in functions[tm]
        for func in functions[tm]:
            parameters = func["params"]
            column = func["column"].lower()
            source = func["source"].split("/")[-1].split('.')[0].lower()
            sql += "ALTER TABLE \"" + source + "\" ADD COLUMN " + column + " VARCHAR;"
            sql += "UPDATE \"" + source + "\" SET " + column + "=" + translate_function_to_sql(parameters, sql) + ");\n"

    return sql


def translate_function_to_sql(parameters, sql):
    function = translate_f_to_sql(parameters['function'])
    sql = function + '('
    for i,param in enumerate(parameters['parameters']):
        if(type(param) is dict):
            sql += translate_function_to_sql(param['value'], sql)
        else:
            value = "'" + param[1]  + "'"
            col = re.findall('\$\(([^)]+)\)', value)
            if(len(col) > 0):
                value = col[0].lower()
            if i < len(parameters['parameters']) - 1:
                sql += value + ','
            else:
                sql += value + ')'
    return sql

def translate_f_to_sql(value):
    if value == "sql:lower":
        sql = "lower"
    elif value == "sql:upper":
        sql = "upper"
    elif value == "sql:concat":
        sql = "concat"
    elif value == "sql:ltrim":
        sql = "ltrim"
    elif value == "sql:replace":
        sql = "replace"
    elif value == "sql:left":
        sql = "left"
    elif value == "sql:right":
        sql = "right"
    elif value == "sql:substring":
        sql = "substr"
    elif value == "sql:regexp_replace":
        sql = "regexp_replace"
    return sql
