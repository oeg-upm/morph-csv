
import re
def translate_fno_to_sql(functions):
    sql = ""
    for tm in functions:
        #if 'query' in functions[tm]
        for func in functions[tm]:
            parameters = func["params"]
            print('**********************************')
            print(str(parameters).replace("'", '"'))
            column = func["column"].lower().replace('-', '_')
            source = func["source"].split("/")[-1].split('.')[0].lower()
            sql += "ALTER TABLE \"" + source + "\" ADD COLUMN " + column + " VARCHAR;"
            sql += "UPDATE \"" + source + "\" SET " + column + "=" + parseFunction(parameters)
            sql += ';'
    return sql
def parseFunction(func):
    parsedFunc = recursiveFuncParser({}, func)
    sql = translateToSql('',parsedFunc)
    return sql
def translateToSql(sql,parsedFunc):
    for el in parsedFunc.keys():
        sql += rmlFunc2sql(el) + '('
        for param in parsedFunc[el]:
            if(type(param) is dict):
                sql += translateToSql('', param) + ','
            else:
                value = "'" + param + "'"
                col = re.findall('\$\(([^)]+)\)', value)
                if(len(col) > 0):
                    value = col[0].lower()
                sql +=  value +  ','
        sql = sql[:-1] + ')'
        return sql
def recursiveFuncParser(sql, func):
    result = sql.copy()
    result[func['function']] = []
    for i,param in enumerate(func['parameters']):
        if(type(param) is dict):
            containedFunc =  recursiveFuncParser({}, param['value'])
            result[func['function']].append(containedFunc)
        elif type(param) is list:
            result[func['function']].append(param[1])
    return result
def rmlFunc2sql(key):
    sql = ''
    if key == "sql:lower":
        sql = "lower"
    elif key == "sql:upper":
        sql = "upper"
    elif key == "sql:concat":
        sql = "concat"
    elif key == "sql:ltrim":
        sql = "ltrim"
    elif key == "sql:replace":
        sql = "replace"
    elif key == "sql:left":
        sql = "left"
    elif key == "sql:right":
        sql = "right"
    elif key == "sql:substring":
        sql = "substr"
    elif key == "sql:regexp_replace":
        sql = "regexp_replace"
    return sql
