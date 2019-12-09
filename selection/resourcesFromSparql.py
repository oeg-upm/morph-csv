import json
from ast import literal_eval
import rdflib
from rdflib.plugins.sparql import *
import re
import yaml
import copy
import sys

def fromSPARQLtoMapping(mapping, query, parsedQuery):
    uris = getUrisFromQuery(parsedQuery)
    print('\n\nURIS:\n\n' + str(uris) + '\n\n\n')
    translatedMapping = simplifyMappingAccordingToQuery(uris,mapping)
#    print('\n\n****************+MAPPNIG************\n\n' + str(translatedMapping).replace('\'', '"'))
    csvColumns = findCsvColumnsInsideTheMapping(translatedMapping)

    return csvColumns, translatedMapping

def getUrisFromQuery(query):
    result = {}
    for el in query['where']:
        if 'patterns' in el.keys():
            for tp in el['patterns']:
                result.update(extractTriplePatternUris(result, tp))
        else:
            result.update(extractTriplePatternUris(result, el))
    return result
def extractTriplePatternUris(result, el):
    if('triples' in el.keys()):
        for tm in el['triples']:
            subject = tm['subject']['value']
            if(subject not in result.keys()):
                result[subject] = {'uris':[], 'fullTM':False}
            if(isUri(subject)):
                result[subject]['uris'].append(subject)
            uri = tm['predicate']['value']
            if(isUri(uri)):
                if uri == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
                    uri = tm['object']['value']
                    result[subject]['uris'].append('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
                result[subject]['uris'].append(uri)
            else:
                uri = tm['object']['value']
                if(isUri(uri)):
                    result[subject]['uris'].append(uri)
                else:
                    result[subject]['fullTM'] = True
    return result

def checkEmptyUris(uris):
    for tm in uris:
        if(len(uris[tm]) > 0):
            return False
    return True

def isUri(uri):
    return str(uri)[:4] == 'http'

def find_triples_in_query(algebra, uris):
    for node in algebra:
        if 'triples' in node:
            for tp in algebra['triples']:
                obtainURISfromTP(tp, uris)
        elif isinstance(algebra[node], dict) and bool(algebra[node].keys()):
            find_triples_in_query(algebra[node], uris)

def obtainURISfromTP(tp, uris):#Simplificable
    if str(tp[0]) not in uris.keys():
        uris[str(tp[0])] = {"predicates": [], "types": []}
    for value in tp:
        if re.match(".*URIRef.*", str(type(value))):
            if str(value) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
                uris[str(tp[0])]["types"].append(str(tp[2]))
            elif str(tp[1]) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and value == tp[1]:
                uris[str(tp[0])]["predicates"].append(str(value))

def simplifyMappingAccordingToQuery(uris, minMapping):
    mapping = substitutePrefixes(minMapping)
    #print('MAPPING:\n' + str(mapping).replace('\'', '"'))
    #sys.exit()
    if(checkEmptyUris(uris)):
        return mapping
    newMapping = {'prefixes':mapping['prefixes'], 'mappings':{}}
    for tm in mapping['mappings']:
        subject = isTmInQuery(mapping['mappings'][tm], uris)
        if(subject['result']):
            if(uris[subject['name']]['fullTM']):
                #print('***********************1*******************')
                if(tm not in newMapping['mappings'].keys()):
                    newMapping['mappings'][tm] = {
                        'sources':mapping['mappings'][tm]['sources'],
                        's':mapping['mappings'][tm]['s'],
                        'po':[]
                        }
                newMapping['mappings'][tm]['po'] = mapping['mappings'][tm]['po']
                #print(str(newMapping).replace('\'', '"'))
            else:
                for po in mapping['mappings'][tm]['po']:
                    if(isPoInUris(po, uris[subject['name']]['uris'])):
                        #print('*****************2*******************+')
                        if(tm not in newMapping['mappings'].keys()):
                            newMapping['mappings'][tm] = {
                                'sources':mapping['mappings'][tm]['sources'],
                                's':mapping['mappings'][tm]['s'],
                                'po':[]
                                }
                        newMapping['mappings'][tm]['po'].append(po)
    #print('MAPPING:\n' + str(newMapping).replace('\'', '"'))                       
    newMapping = removeEmptyTM(newMapping)
    newMapping  = addReferencesOfTheJoins(mapping, newMapping)
    return newMapping

def checkIsUriType(uris):
    return (len(uris) == 2 and
             "a" in uris
            )

def isTmInQuery(tm, uris):
    tmUris = getUrisFromTM(tm)
    result = False
    subjectName = ''
    #print('********************TM URIS*****************')
    #print(tmUris)
    for subject in uris.keys():
        if len(list(set(tmUris) & set(uris[subject]['uris']))) == len(uris[subject]['uris']):
            result = True
            subjectName = subject
            break
    return {'result':result,'name':subjectName}

def getUrisFromTM(tm):
    result = [tm['s']]
    for po in tm['po']:
        if(type(po) is list):
            result.extend(po)
        else:
            result.append(po['p'])
    return result

def addReferencesOfTheJoins(oldMapping, mapping):
    #print('***************NO REFERENCES MAPPING**********:\n\n\n' + str(mapping).replace('\'', '"'))
    newMapping = {'prefixes':mapping['prefixes'], 'mappings':mapping['mappings']}
    tmReferences = {}
    for tm in mapping['mappings']:
        for po in mapping['mappings'][tm]['po']:
            if type(po) is dict:
                for o in po['o']:
                    tmReferences.update(checkIfReferenceIsDefined(tmReferences,oldMapping,mapping,o))
    newMapping['mappings'].update(tmReferences)
    return newMapping

def checkIfReferenceIsDefined(storedTm,oldMapping,mapping,o):
    newMapping = mapping.copy()
    #print('\n\nO:\n\n' + str(o))
    joinReferences = getJoinReferences(o)
    tmName = o['mapping']
    #print('\n\n\nJOIN REFERENCES:\n\n\n' + str(joinReferences))
    tmReference = joinReferences['outerRef']
    if(tmName not in storedTm.keys()):
        storedTm[tmName] = oldMapping['mappings'][tmName]
        storedTm[tmName]['po'] = []
        if(tmName in mapping['mappings'].keys()):
            storedTm[tmName] = mapping['mappings'][tmName]
    if (joinReferences['outerRef'] not in getColPatterns(newMapping['mappings'][tmName]) and
        joinReferences['outerRef'] not in getColPatterns(storedTm[tmName])
            ):
        #print('BUSCAMOS:' + str(joinReferences['outerRef']))
        for i,po in enumerate(oldMapping['mappings'][o['mapping']]['po']):
            if(joinReferences['outerRef'] in getColPatterns(po)):
                #print('Hay que añadir a: \n' + str(po))
                storedTm[tmName]['po'].append(po)
    return storedTm

def getJoinReferences(join):
    result = {'innerRef': join['condition']['parameters'][0][1], 'outerRef':join['condition']['parameters'][1][1]}
    return result
def removeUnnecesaryTM(mapping):
    #print('MAPPING:\n' + str(mapping).replace('\'', '"'))
    tripleMaps = mapping['mappings'].keys()
    newMapping = mapping.copy()
    newMapping = removeEmptyTM(newMapping)
    return newMapping

def removeEmptyTM(mapping):
    #print('MAPPING:\n' + str(mapping).replace('\'','"'))
    newMapping = mapping.copy()
    tmToRemove = []
    types = [ po[1] 
            for tm in mapping['mappings']
            for po in mapping['mappings'][tm]['po']
            if (type(po) is list and po[0] == 'a')
            ]
    for tm in mapping['mappings']:
        #print('PO:\n' + str(mapping['mappings'][tm]['po']))
        if(len(mapping['mappings'][tm]['po']) == 1 and 
            type(mapping['mappings'][tm]['po'][0]) is list and
            mapping['mappings'][tm]['po'][0][0] == 'a'
            and types.count(mapping['mappings'][tm]['po'][0][1]) > 1):
            types.pop(types.index(mapping['mappings'][tm]['po'][0][1]))
            tmToRemove.append(tm)
    for tm in tmToRemove:
        del newMapping['mappings'][tm]
    return newMapping

def findCsvColumnsInsideTheMapping(mapping):
    columns = {}
    for tm in mapping['mappings']:
        columns[tm] = {
                'source':str(mapping['mappings'][tm]['sources'][0]).split('/')[-1:][0].split('~')[0],
                'columns':[]
                }
        columns[tm]['columns'].extend(cleanColPattern(mapping['mappings'][tm]['s']))
        for po in mapping['mappings'][tm]['po']:
            if(type(po) is dict):
                for o in po['o']:
                    references = getJoinReferences(o)
                    colReference = cleanColPattern(references['innerRef'] )
                    if(not bool(set(colReference)& set(columns[tm]['columns']))):
                        columns[tm]['columns'].extend(cleanColPattern(references['innerRef']))
            else:
                matches = cleanColPattern(po)
                columns[tm]['columns'].extend(matches)
        columns[tm]['columns'] = list(set(columns[tm]['columns']))
    return columns

def getColPatterns(element): 
    colPattern  = '\$\(([^)]+)\)'
    matches = re.findall(colPattern, str(element))
    result = [ '$(' + str(match) + ')' for match in matches]
    return result

def cleanColPattern(columns):
    if type(columns) is dict:
        columns = [columns]
    columns = getColPatterns(columns)
    #print('COLUMNS:' + str(columns))
    result = []
    for col in columns:
        result.append(str(col)[2:-1])
    return result

def isPoInUris(po, uris):
    for item in po:
        if item in uris:
            return True
    return False


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
            else:
                parentColumns = getColumnsfromOM(join[joinscount]["condition"]["parameters"][i][1])
                parent = join[joinscount]["mapping"]
        joinscount += 1
    return columns, parentColumns, parent


def substitutePrefixes(mapping):
    prefixes = mapping["prefixes"]
    strMapping = str(mapping['mappings'])
    for prefix in prefixes:
        strMapping = strMapping.replace('\'' + prefix + ':', '\'' + prefixes[prefix])
#    strMapping = strMapping.replace('\'','"')
    expandedMapping  = dict(literal_eval(strMapping))
    for tm in expandedMapping:
        for index,po in enumerate(expandedMapping[tm]['po']):
            if type(po) is list and po[0] == 'a':
                expandedMapping[tm]['po'][index][0] = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'
    newMapping = {'prefixes':prefixes,'mappings':dict(expandedMapping)}
    return newMapping

def atomicprefixsubtitution(prefixes, value):
    aux = value.split(":")
    for prefix in prefixes.keys():
        if aux[0] == prefix:
            aux[0] = prefixes[prefix]
            break
    return aux


def getColumnsFromFunctions(csvColumns, functions):
    for tm in functions:
        for func in functions[tm]:
            if(tm in csvColumns.keys()):
                for csv in csvColumns:
                    sourceColumns = csvColumns[tm]["columns"]
                    for column in sourceColumns:
                        if column in func['column']:
                            columns = cleanColPattern(functions[tm])
#                            extractReferencesFromFno(functions[tm][column], columns)
                            csvColumns[tm]["columns"].remove(column)
                            csvColumns[tm]["columns"].extend(columns)
                            csvColumns[tm]["columns"] = list(dict.fromkeys(csvColumns[tm]["columns"]))
    return csvColumns


def extractReferencesFromFno(functions, columns):
    if 'parameter' in functions:
        functions = functions["value"]
    for parameters in functions["parameters"]:
        if 'parameter' in parameters:
            extractReferencesFromFno(parameters, columns)
        else:
            if re.match("\\$\\(.*\\)", parameters[1]):
                columns.extend(getColumnsfromOM(parameters[1]))


# From a dict with sources a columns name, return the same dict with the indexes of the columns
def getIndexFromColumns(csvColumns, all_columns):
    #print(csvColumns)
    #print(all_columns)
    result = {}
    for tm in all_columns:
        result[csvColumns[tm['source']]['source']] = []
        for col in csvColumns[tm['source']]['columns']:
            result[csvColumns[tm['source']]['source']].append(tm['columns'].index(col))
    #
    # for tm in csvColumns:
    #    columns = csvColumns[tm]["columns"]
    #    source = csvColumns[tm]["source"]
    #    aux = []
    #    for file in all_columns:
    #        if file["source"] == source:
    #
    #            for column in columns:
    #                aux.extend(file["columns"].index(column))
    #    csvColumns[tm][columns] = aux
    return result
