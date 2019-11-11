#/bin/python3
import json
import sys
import os

emptyValues = {'', ' '}

def jsonLoader(path):
    try:
        result = json.loads(open(path).read())
        return result
    except Exception as e:
        print(e)
        print("The path is not valid")
        sys.exit()
def jsonIterator(json):
    try:
        result = {'values':[]}
        if('tables' in json.keys()):
            for table in json['tables']:
                element = {}
                element['url'] = getUrl(table)
                element['titles'] = getTitles(table)
                element['delimiter'] = getDelimiter(table)
                element['skipRows'] = getSkipRows(table)
                element['null'] = getNullValue(table)
                element['max'] = getExtremes(table,['maximum', 'maxInclusive'], ['maxExclusive'])
                element['min'] = getExtremes(table, ['minimum', 'minInclusive'], ['minExclusive'])
                element['dateFormat'] = getFormat(table, 'date')
                element['booleanFormat'] = getFormat(table, 'boolean')
                result['values'].append(element)
                printTitles(element)
            return result
        else:
            raise Exception("Invalid file, wrong format")
    except Exception as e:
        print('The CSVW is not valid')

def printTitles(data):
    print('*************' + str(data['url']) + '***********************')
#    print(data['titles'])
    aux = '\'' + str(data['titles']).replace("[", "").replace("]", "").replace("\'", "") + '\''
    print(aux)
    os.system('./functions.sh %s'%(aux))

def getUrl(table):
    try:
        if('url' in table.keys() and str(table['url']) not in emptyValues):
            return str(table['url'])
        else:
            raise Exception("The format of CSVW is wrong, the Url is not valid")
    except Exception as e:
        print(e)
        sys.exit()

def getTableTitles(table):
    try:
        titles = []
        if('rowTitles' in table.keys() and str(table['rowTitles']) not in emptyValues):
            titles = table['rowTitles']
        elif('rowTitle' in table.keys() and str(table['rowTitle']) not in emptyValues):
            title  = table['rowTitle']
        elif(columnsChecker(table)):
            for col in table['tableSchema']['columns']:
                if('titles' in col.keys()):
                    if( type(col['titles']) is str and col['titles'] not in emptyValues):
                        titles.append(str(col['titles']))
                    elif(type(col['titles']) is list and len(col['titles']) > 0):
                        titles = titles + col['titles']
                elif('title' in col.keys()):
                    if(type(col['title']) is str and col['title'] not in emptyValues):
                        titles.append(str(col['title']))
                    elif(type(col['title']) is list and len(col['title']) > 0):
                        titles = titles + col['title']
        return titles

    except Exception as e:
        print(e)
        pass

def getTitles(table):
    titles = getTableTitles(table)
    result = ''.join(str(titles[i]) + ',' for i in range(0, len(titles) - 1)) + titles[-1:][0]
    return result

def getDelimiter(table):
    try:
        delimiter = ','
        if('dialect' in table.keys() and type(table['dialect']) is dict and 'delimiter' in table['dialect'].keys() and str(table['dialect']['delimiter']) != ''):
            delimiter = ord(table['dialect']['delimiter'])
        return delimiter
    except Exception as e:
        print(e)

def getSkipRows(table):
    skipRows = 0
    if('dialect' in table.keys() and 'skipRows' in table['dialect'].keys()):
        skipRows = int(table['dialect']['skipRows'])
    return skipRows

def getNullValue(table):
    nullValues  = [] 
    if(columnsChecker(table)):
        for col in table['tableSchema']['columns']:
            if('null' in col.keys()):
                nullValues.append(col['null'])
            else:
                nullValues.append('')
    return nullValues
def getExtremes(table, inclusive, exclusive):
    extremes  = {'inclusive':[],'exclusive':[]}
    if(columnsChecker(table)):
        for col in table['tableSchema']['columns']:
            for el in inclusive:
                if(el in col.keys()):
                    extremes['inclusive'].append(col[el])
                    break
            for el in exclusive:
                if(el in col.keys()):
                    extremes['exclusive'].append(col[el])
                    break
    return extremes

def getFormat(table, dataType):
    try:
        result = []
        if(columnsChecker(table)):
            for indx, col in enumerate(table['tableSchema']['columns']):
                if('datatype' in col.keys()):
                    if(type(col['datatype']) is str and col['datatype'] == dataType and 'format' in col.keys()):
                        result.append({indx:col['format']})
                    elif(type(col['datatype']) is dict and 'base' in col['datatype'] and 'format' in col['datatype'] and col['datatype']['base'] == dataType):
                        result.append({str(indx):col['datatype']['format']})
        return result
    except Exception as e:
        print(e)

def columnsChecker(table):
    return 'tableSchema'in table.keys() and 'columns' in table['tableSchema'].keys() and type(table['tableSchema']['columns']) is list and len(table['tableSchema']['columns']) > 0



def main():
    csvw = jsonLoader("../mappings/madridGtfs.csvw.json")
    csvwParsed = jsonIterator(csvw)
    #print(str(csvwParsed).replace("\'","\""))

#main()
