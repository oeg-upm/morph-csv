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
        sys.exit()
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
    #print('PREDICATE:' + str(predicate) + '\nVARIABLE:' + str(variable) + '\nColumn:' + str(column))
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
    mapping["mappings"][column] = {"source": source, "s": s, "po": pom}
    return mapping

def createJoin(predicate, column):
    join = {}
    parameters = [["str1", column], ["str2", "$(id)"]]
    join["p"] = predicate
    join["o"] = [{"mapping": column, "condition:": {"function": "equal", "parameters": parameters}}]
    return join

def dataTranslation(data, delimiter, path):
    #print('SCRIPT:\n' + str(data['script']) + '\nCOLS:\n' + str(data['columns']))
    os.system("bash bash/fn1.sh '%s' '%s' '%s'"%(str(delimiter), str(data['script']), str(path)))

def getPredicateAndObjectFromQuery(query, mapping,parsedQuery,column):
    print('SEARCHING: '  + column)
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
        print("FALLA getPredicateFromQuery ")
        print(traceback.format_exc())
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
    print("PREDICATE: \n" + str(value))
    print('PREFIXES: \n' + str(prefixes))
    if(len(value.split(":")) == 2):
        aux = value.split(":")
        for prefix in prefixes.keys():
            if aux[0] == prefix:
                aux[0] = prefixes[prefix]
                break
        print('RESULT:\n' + str(aux))
        return aux
    return value

def find_object_in_query(algebra, predicate):
    print('ALGEBRA\n' + str(algebra))
    for node in algebra:
        if 'triples' in node:
            for tp in algebra['triples']:
                if re.match(predicate, tp[1]):
                    return tp[2]
        elif isinstance(algebra[node], dict) and bool(algebra[node].keys()):
            find_object_in_query(algebra[node], predicate)

def toThirdNormalForm(mapping):

    equal = {}
    normalize = []
    for tm in mapping["mappings"]:
        for pom in mapping["mappings"][tm]["po"]:
            if 'p' in pom:
                source = mapping["mappings"][tm]["sources"][0][0]
                parent_mapping = mapping["mappings"][tm]["po"]["o"]["mapping"]
                source_parent = mapping["mappings"][parent_mapping]["sources"][0][0]
                if source == source_parent:
                    for i in range(len(mapping["mappings"][tm]["po"]["o"]["condition"]["parameters"])):
                        if mapping["mappings"][tm]["po"]["o"]["condition"]["parameters"][i][0] == "str2":
                            reference = getColumnsfromOM(mapping["mappings"][tm]["po"]["o"]["condition"]["parameters"][i][1])
                            equal[parent_mapping] = reference[0]

    for tm in equal:
        target = tm
        source = mapping["mappings"][tm]["sources"][0][0]
        columns = []
        pomcount = 0
        for pom in mapping["mappings"][tm]["pom"]:
            if 'p' in pom:
                columns.extend(getColumnsfromJoin(mapping["mappings"][tm]["po"][pomcount]["o"]))
            else:
                columns.extend(getColumnsfromOM(mapping["mappings"][tm]["po"][pomcount][1]))
            pomcount += 1

        remove = columns.copy().pop(equal[tm])
        mapping["mappings"][tm]["sources"][0][0] = "./tmp/csv/"+target+".csv~csv"
        normalize.extend({"source": source, "remove": remove, "columns": columns, "target": target})

    """
        normalize content:
            - source: the name of the file where you can get the columns
            - remove: the columns you have to remove from source
            - target: the name of the new file
            - columns: the columns you have to add to target
        
    """
    # ToDo: execute bash script to create target and remove the "remove" columns from source



def getColumnsfromOM(om):
    columns = []
    aux = om.split("$(")
    for references in aux:
        if re.match(".*\\).*", references):
            columns.append(references.split(")")[0])
    return columns

def getColumnsfromJoin(join):
    columns = []
    joinscount = 0
    while joinscount < len(join):
        for i in [0, 1]:
            if join[joinscount]["condition"]["parameters"][i][0] == "str1":
                columns.extend(getColumnsfromOM(join[joinscount]["condition"]["parameters"][i][1]))
        joinscount += 1
    return columns
