
import re

def translate_fno_to_sql(functions):
    sql = ""
    for tm in functions:
        if 'query' in functions[tm]:
            f = ""
            function = functions[tm]["fno"]["params"]
            column = function[tm]["fno"]["column"]
            source = re.sub("\\.csv~csv", "", functions["tm"]["fno"]["source"].split("/")[-1]).upper()
            sql += "ALTER TABLE " + source + "ADD COLUMN (" + column + " VARCHAR(200));\n"
            sql += "UPDATE " + source + "SET " + column + "=" + translate_function_to_sql(function, f) + ";\n"

    return sql


def translate_function_to_sql(function, sql):

    for f in range(len(function)):
        sql += translate_f_to_sql(function[f]) + "("
        for i in range(len(function[f]["parameters"])):
            if isinstance(function[f]["parameters"][i], dict):
                translate_function_to_sql(function[f]["parameters"][i]["value"], sql)
            else:
                param = function[f]["parameters"][i][1]
                if re.match("\\$\\(.*\\)", param):
                    param = re.sub("\\)", "", re.sub("\\$\\(", "", param))
                if i == len(function[f]["parameters"])-1:
                    sql += param + ")"
                else:
                    sql += param + ","

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