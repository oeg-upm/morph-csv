#/bin/python3
import json
import sys

emptyValues = {'', ' '}

def jsonLoader(path):
    try:
        result = json.loads(open(path).read())
        return result
    except Exception as e:
        print("The path is not valid")
        sys.exit()
def jsnoIterator(json):
    try:
        result = []
        if('tables' in json.keys()):
            for table in json['tables']:
                element = {}
                element['url'] = getUrl(table)
                element['titles'] = getTitles(table)
                element['delimiter'] = getDelimiter(table)
                element['skipRows'] = getSkipRows(table)
                element['null'] = getNullValue(table)
                element['max'] = getMax(table)
                element['min'] = getMin(table)
                element['dateFormat'] = getDateFormat(table)
                element['booelanFormat'] = getBooleanFormat(table)
                element['dateCols'] = getDateCols(table)
                element['booleanCols'] = getBooleanCols(table)
    except Exception as e:
        print('The CSVW is not valid')

def getUrl(table):
    try:
        if('url' in table.keys() and str(table['url']) not in emptyValues]):
            return str(table['url'])
        else:
            raise Exception("The format of CSVW is wrong, the Url is not valid")
    except Exception as e:
        print(e)
        sys.exit()

def getTitles(table):
    try:
        titles = []
        if('rowTitles' in table.keys() and str(table['rowTitles']) not in emptyValues):
            titles = table['rowTitles']
        elif('rowTitle' in table.keys() and str(table['rowTitle']) not in emptyValues):
            title  = table['rowTitle']
        elif('columns' in table.keys() and str(table['columns']) not in emptyValues):
            for col in table['columns']:
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

def getDelimiter(table):
    try:
        delimiter = ','
        if('dialect' in table.keys() and 'delimiter' in table['dialect'].keys()):
            delimiter = str(table['dialect']['delimeter'])
        return delimiter
    except Exception as e:
        print(e)
        pass

def getSkipRows(table):
    skipRows = 0
    if('dialect' in table.keys() and 'skipRows' in table['dialect'].keys()):
        skipRows = int(table['dialect']['skipRows'])
    return skipRows

def getNullValue(table):
    
