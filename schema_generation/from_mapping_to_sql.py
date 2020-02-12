import re
import sys
import clean.csvwParser as csvwParser
import schema_generation.creation_sql_alters as function
import selection.resourcesFromSparql as resourcesFromSparql

# return true if there is a join in the mapping, hence, in the query, if not morph-rdb in csv mode should be run

def decide_schema_based_on_query(mapping):
    for tm in mapping["mappings"]:
        for pom in mapping["mappings"][tm]["po"]:
            # if p in pom means there is a join in the mapping
            if 'p' in pom:
                return True
    return False


def generate_sql_schema(csvw,mapping,decision):
#print('****************MAPPNIG********************\n' + str(mapping).replace("'", '"'))
    sqlGlobal = ""
    foreignkeys = ""
    indexes = ""
    alters = ""
    for i,table in enumerate(csvw["tables"]):
        sql = ''
        source = csvwParser.getUrl(table).split("/")[-1:][0].replace(".csv","").lower()
        columns = csvw["tables"][i]["filteredRowTitles"]
        sql += "DROP TABLE IF EXISTS \"" + source + "\" CASCADE;"
        sql += "CREATE TABLE " + source + "("
        foreignKeyList = getForeignKeys(table)
        for columName in columns :
            sql += columName + " " + find_type_in_csvw(columName, table["tableSchema"]) + ","
#            if(columName in foreignKeyList and not ('primaryKey' in table['tableSchema'].keys() and columName in table['tableSchema']['primaryKey'])):
#                sql = sql[:-1] + " UNIQUE,"

        if decision:
            try:
                primarykeys = table["tableSchema"]["primaryKey"]
            except:
                primarykeys = ''
            if len(primarykeys) > 0:
                sql += "PRIMARY KEY (" + primarykeys + "),"
            else:
                indexes += ''.join("CREATE INDEX IF NOT EXISTS " + col + "_index ON " + source + " ( " + col + ");" for col in getColumnsFromSubject(mapping, findTMofTable(mapping,source)))
#                indexes += "CREATE INDEX IF NOT EXISTS subject_cols_index_"+ source + "  ON " + source + " ( " + getColumnsFromSubject(mapping, findTMofTable(mapping,source))  + " );"
            if 'foreignKey' in table['tableSchema'].keys():
                for fk in table["tableSchema"]["foreignKey"]:
                    column = fk["columnReference"]
                    refTable = fk["reference"]["resource"].split("/")[-1].replace(".csv","")
                    reference = fk["reference"]["columnReference"]
                    if(isDefinedReference(mapping,findTMofTable(mapping, refTable), reference)):
                        if(isPrimaryKey(csvw, reference, refTable)):
                                foreignkeys += "ALTER TABLE " + source +  " ADD FOREIGN KEY ("+column.lower()+") REFERENCES "+refTable.lower()+" ("+reference.lower()+");"
                        else:
                             indexes += "CREATE INDEX IF NOT EXISTS " + reference + "_index  ON " + refTable.lower() + " (" + reference + ");"


        sql = sql[:-1] + ");"
        sqlGlobal += sql
    alters += foreignkeys
    alters += indexes
#    sqlGlobal += function.translate_fno_to_sql(functions)
    #print('***********FUNCTIIONS**********')
    #print(str(functions).replace('\'','"'))
#    print('***********SCHEMA**************')
#    print(sqlGlobal.replace(';', ';\n'))
    return sqlGlobal, alters

def isPrimaryKey(csvw,column, tableName):
    for table in csvw['tables']:
        if(csvwParser.getUrl(table).split("/")[-1].replace(".csv", "") == tableName and
          'primaryKey' in table['tableSchema'].keys() and
          column == table['tableSchema']['primaryKey']
          ):
            return True
    return False

def getForeignKeys(table):
    result = []
    if 'foreignKey' in table['tableSchema']:
        for fk in table['tableSchema']['foreignKey']:
                result.append(fk["columnReference"])
    return result
def getColumnsFromSubject(mapping, TM):
    subject = mapping['mappings'][TM]['s']
    return resourcesFromSparql.cleanColPattern(subject)

def findTMofTable(mapping, table):
        for tm in mapping['mappings']:
                if(table.lower() in str(mapping['mappings'][tm]['sources']).lower()):
                        return tm
        return 'Null'
def isDefinedReference(mapping,tm, reference):
        if tm is not 'Null':
                colPattern = '\$\(([^)]+)\)'
                matches = re.findall(colPattern, str(mapping['mappings'][tm]))
                if(reference in matches):
                        return True
        return False
def find_type_in_csvw(title, csvw_columns):
    datatype = "VARCHAR"
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
        translated_type = "VARCHAR"

    return translated_type
