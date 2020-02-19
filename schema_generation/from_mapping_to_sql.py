import re
import os
import sys
import clean.csvwParser as csvwParser
import schema_generation.creation_sql_alters as function
import selection.resourcesFromSparql as resourcesFromSparql

#IndexTrigger is the minimum selectivity value required to create an index
indexTrigger = 0.70

# return true if there is a join in the mapping, hence, in the query, if not morph-rdb in csv mode should be run

def decide_schema_based_on_query(mapping):
    for tm in mapping["mappings"]:
        for pom in mapping["mappings"][tm]["po"]:
            # if p in pom means there is a join in the mapping
            if 'p' in pom:
                return True
    return False


def generate_sql_schema(csvw,mapping,decision):
   # print('****************MAPPNIG********************\n' + str(mapping).replace("'", '"'))
    sqlGlobal = ""
    foreignkeys = ""
    indexes = ""
    alters = ""
    calculatedSelectivity = {}
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
                result = generateSubjectIndexes(source, mapping, table, calculatedSelectivity)
                indexes += result["indexes"]
                calculatedSelctivity = result["selectivity"]
            if 'foreignKey' in table['tableSchema'].keys():
                for fk in table["tableSchema"]["foreignKey"]:
                    column = fk["columnReference"]
                    refTable = fk["reference"]["resource"].split("/")[-1].replace(".csv","").lower()
                    reference = fk["reference"]["columnReference"]
                    if(isDefinedReference(mapping,findTMofTable(mapping, refTable), reference)):
                        if(isPrimaryKey(csvw, reference, refTable)):
                            foreignkeys += "ALTER TABLE " + source +  " ADD FOREIGN KEY ("+column.lower()+") REFERENCES "+refTable+" ("+reference.lower()+");"
                        else:
                            if(refTable not in calculatedSelectivity.keys()):
                                calculatedSelectivity[refTable] = []
                            selectivity = 0.0
                            if(reference not in calculatedSelectivity[refTable]):
                                selectivity = calculateSelectivity(refTable, reference, csvwParser.findTableByUrl(refTable, csvw))
                                calculatedSelectivity[refTable].append(reference)
                            if  selectivity >= indexTrigger:
                                indexes += "CREATE"
                                if selectivity == 1.0:
                                    indexes += " UNIQUE"
                                indexes += " INDEX IF NOT EXISTS " + reference + "_index_" + refTable + "  ON " + refTable.lower() + " (" + reference + ");"


        sql = sql[:-1] + ");"
        sqlGlobal += sql
    alters += foreignkeys
    alters += indexes
#    sqlGlobal += function.translate_fno_to_sql(functions)
    #print('***********FUNCTIIONS**********')
    #print(str(functions).replace('\'','"'))
#    print('***********SELECTIVITY**************')
#    print(sqlGlobal.replace(';', ';\n'))
#    print(calculatedSelectivity)
    return sqlGlobal, alters
def generateSubjectIndexes(source, mapping, table, calculatedSelectivity):
    indexes = ""
    selectivity = 0.0
    for col in  getColumnsFromSubject(mapping, findTMofTable(mapping,source)):
        if(source.lower() not in calculatedSelectivity.keys()):
            calculatedSelectivity[source] = []
        if col not in calculatedSelectivity[source.lower()]:
            selectivity = calculateSelectivity(source,col, table)
            calculatedSelectivity[source.lower()].append(col)
        else:
            selectivity = 0.0
        if  selectivity >= indexTrigger:
            indexes += "CREATE"
            if selectivity == 1.0:
                indexes += " UNIQUE"
            indexes += " INDEX IF NOT EXISTS " + col + "_index_" + source  + " ON " + source + " (" + col + ");"
    return {"indexes":indexes, "selectivity":calculatedSelectivity}
def calculateSelectivity(source, colName, table):
    if(not table is None):
        source = csvwParser.getUrl(table).split("/")[-1]
        print('SOURCE: ' + source + 'COLNAME: ' + colName)
        awkCol = "$" + str(table['filteredRowTitles'].index(colName) + 1)
        path = 'tmp/csv/' + source
        selectivity = 0.0
        os.system('bash bash/selectivityCalculator.sh \'%s\' \'%s\''%(path, awkCol))
        with open('tmp/selectivity.tmp.txt', "r") as f:
            selectivity = float(f.readline())
        print("The column %s from  %s has a selecivity of: %s"%(colName, source, selectivity))
        return selectivity
    else:
        return False
def isPrimaryKey(csvw,column, tableName):
#    print('TABLE NAME:%s'%(tableName))
#    print('COLUMN:%s'%(column))
    for table in csvw['tables']:
        if(csvwParser.getUrl(table).split("/")[-1].replace(".csv", "").lower() == tableName and
          'primaryKey' in table['tableSchema'].keys() and
          column == table['tableSchema']['primaryKey'].lower()
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
