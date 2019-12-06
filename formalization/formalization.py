#!/bin/python3
import re
import os
import sys
from rdflib.plugins.sparql import *
from clean import csvwParser as csvwParser
import traceback

def addNormalizedTablesToCsvw(csvw, mapping, query, parsedQuery):
    newTables = []
#   query = queryPrefixRewritter(query, mapping['prefixes'])
    for table in csvw['tables']:
        cols = csvwParser.getCols(table)
        for col in cols:
            if(csvwParser.hasSeparator(col)):
                colName = csvwParser.getColTitle(col)
                newTables.append(createNewTable(table,col))
                predicate,variable =getPredicateAndObjectFromQuery(query, mapping, parsedQuery,colName)
                #sys.exit()
                query = queryRewritten(query,predicate,variable,colName)
                mapping = mappingTranslation(mapping, colName)
        dataTranslation(csvwParser.getSeparatorScripts(table),
                csvwParser.getDelimiterValue(table),
                csvwParser.getUrl(table).split("/")[-1:][0])
    csvw['tables'].extend(newTables)
    result = {'csvw':csvw, 'mapping':mapping, 'query':query}
    return result

def createNewTable(table,col):
    table = {
        'url':'ALGO/%s.csv'%(csvwParser.getColTitle(col)),
        'dialect':{
            'delimiter':csvwParser.getDelimiterValue(table),
            'header':False
            },
        'tableSchema':{
            'rowTitles':['id', 'value'],
            'columns':[
                {
                    'titles':'value',
                    'null':csvwParser.getNullValue(col),
                    'datatype':csvwParser.getDataType(col)
                    }
                ]
            }
        }
    return table
        
def toSecondNormalForm(mapping, column, query):
    #Requirements for NORMALIZATION: csvw, yarrrmlMapping, sparqlQuery.
    mappingTranslation(mapping, column)
    queryRewritten(query, getPredicateAndObjectFromQuery(query, column, mapping), column)

def queryRewritten(query, predicate, variable, column):
    ##print('PREDICATE:' + str(predicate) + '\nVARIABLE:' + str(variable) + '\nColumn:' + str(column))
    query = query.replace("?" + variable, "?"+column+".\n\t?"+column+"<ex:"+column+"> ?"+variable)
    return query

def mappingTranslation(mapping, column):
    for tm in mapping["mappings"]:
        i = 0
        for pom in mapping["mappings"][tm]["po"]:
            if re.match("\\$\\("+column+"\\)", mapping["mappings"][tm]["po"][i][1]):
                mapping["mappings"][tm]["po"][i] = createJoin(mapping["mappings"][tm]["po"][i][0], column)
        i += 1

    source = [["./tmp/csv/"+column + '.csv']]
    s = "http://example.com/$(id)-$("+column+")"
    pom = [["ex:"+column, "$(value)"]]
    mapping["mappings"][column] = {"sources": source, "s": s, "po": pom}
    return mapping

def createJoin(predicate, column):
    join = {}
    parameters = [["str1", column], ["str2", "$(id)"]]
    join["p"] = predicate
    join["o"] = [{"mapping": column, "condition:": {"function": "equal", "parameters": parameters}}]
    return join

def dataTranslation(data, delimiter, path):
    if(len(data['columns'])>0):
        ##print('SCRIPT:\n' + str(data['script']) + '\nCOLS:\n' + str(data['columns']))
        os.system("bash bash/fn2.sh '%s' '%s' '%s'"%(str(delimiter), str(data['script']), str(path)))

def getPredicateAndObjectFromQuery(query, mapping,parsedQuery,column):
    #print('SEARCHING: '  + column)
    predicate = getPredicateFromQuery(query, column, mapping)
    pObject = getObjectFromQuery(parsedQuery, predicate)
    return predicate, pObject
    
def getPredicateFromQuery(query, column,mapping):
    predicate = ''
    try:
        for tm in mapping["mappings"]:
            for pom in mapping["mappings"][tm]["po"]:
                if re.match("\\$\\("+column+"\\)", pom[1]):
                    predicate = pom[0]
        return predicate
    except:
        #print("FALLA getPredicateFromQuery ")
        #print(traceback.format_exc())
        sys.exit()


def getObjectFromQuery(parsedQuery, predicate):
    pObject = ''
    for tp in parsedQuery['where']:
        for bgp in tp['triples']:
            if(predicate == str(bgp['predicate']['value'])):
                pObject = bgp['object']['value']
    return pObject

def queryPrefixRewritter(query, prefixes):
    for prefix in prefixes:
        query = str(query).replace(str(prefix)+':', str(prefixes[prefix]))
    return query

def atomicprefixsubtitution(prefixes, value):
    #print("PREDICATE: \n" + str(value))
    #print('PREFIXES: \n' + str(prefixes))
    if(len(value.split(":")) == 2):
        aux = value.split(":")
        for prefix in prefixes.keys():
            if aux[0] == prefix:
                aux[0] = prefixes[prefix]
                break
        #print('RESULT:\n' + str(aux))
        return aux
    return value

def find_object_in_query(algebra, predicate):
    #print('ALGEBRA\n' + str(algebra))
    for node in algebra:
        if 'triples' in node:
            for tp in algebra['triples']:
                if re.match(predicate, tp[1]):
                    return tp[2]
        elif isinstance(algebra[node], dict) and bool(algebra[node].keys()):
            find_object_in_query(algebra[node], predicate)

def toThirdNormalForm(mapping, csvColumns, csvw):
    fn3Tm = findTmWithSameSource(csvColumns)
    fn3Tm = findTmWithDistinctSubject(fn3Tm, mapping)
    fn3Tm = findColumnsOfFN3Tm(fn3Tm, csvColumns)
    #Scope: Encontrar los TM que comparten el mismo source y cuyos sujetos son diferentes.
    #HowTo: 
    '''
        1º Encontrar Fuentes Duplicadas DONE
        2º Guardar los nombres del TM comparten fuente DONE
        3º Guardar las csvColumns de cada TM al que hay que aplicar FN3 DONE
        4º Llamar al bashScript fn3.sh para generar n CSVs nuevos cada uno con su columna
           correspondiente en base al Mapping
    '''
    #print('\n\n\n***********************FN3tm********************\n\n\n')
    #print(str(fn3Tm).replace('\'', '"') + '\n\n\n')
#    csvw = obtainFN3NormalizedCsvw(csvw, fn3Tm) 
#    script  = getFn3FormalizationScript(csvw, fn3Tm) 
    #TODO: Execute bash script to create target and remove the "remove" columns from source.
    #TODO: MODIFY CSVW TO APPEND THE NEW TABLES 


def findTmWithDistinctSubject(sources, mapping):
    result =  {}
    for source in sources:
        #TODO QUE PASA SI HAY 3 TM CON EL MISMO 
        #SOURCE PERO SOLO 2 DE ELLOS TIENEN DISTINTO SUBJECT?
        #DE MOMENTO SUPONEMOS QUE SOLO SE VA A DAR EL CASO DE QUE
        #SOLO HAY 2 TM QUE COMPARTAN EL MISMO SOURCE. SI FALLA ES POR ESO :)
        if(mapping['mappings'][sources[source][0]] != mapping['mappings'][sources[source][1]]):
            result[source] = sources[source]
    return result
def findTmWithSameSource(csvColumns):
    result = {}
    for tm in csvColumns:
        if csvColumns[tm]['source'] not in result.keys():
            result[csvColumns[tm]['source']] = []
        result[csvColumns[tm]['source']].append(tm)
    return result

def findColumnsOfFN3Tm(sources, csvColumns):
    result = {}
    for source in sources:
        result[source] = {}
        for tm in sources[source]:
            result[source][tm] = csvColumns[tm]['columns']
    return result
def getColumnsfromOM(om):
    om = str(om).replace('$(', '').replace(')', '').split(' ')
    #print(om)
    return om
    '''
    columns = []
    aux = om.split("$(")
    for references in aux:
        if re.match(".*\\).*", references):
            columns.append(references.split(")")[0])
    return columns
    '''
def getColumnsfromJoin(join):
    columns = []
    joinscount = 0
    while joinscount < len(join):
        for i in [0, 1]:
            if join[joinscount]["condition"]["parameters"][i][0] == "str1":
                columns.extend(getColumnsfromOM(join[joinscount]["condition"]["parameters"][i][1]))
        joinscount += 1
    return columns
