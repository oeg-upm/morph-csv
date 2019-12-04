import json
import sys
import os
import csv

#Valores nulos que se usan para verificar la validez de los datos.
emptyValues = ['', ' ']
rowTitles = []
filteredRowTitles = []
#Carga el CSVW en el DataFrame
def jsonLoader(path):
    try:
        result = json.loads(str(open(path).read()))
        return result
    except Exception as e:
        print(e)
        sys.exit()
def filterCols(table):
    columns = []
    if(columnsChecker(table)):
        for col in table['tableSchema']['columns']:
            if(str(getColTitle(col)) in table['filteredRowTitles']):
                columns.append(col)
        table['tableSchema']['columns'] = columns
    return table

def insertRowTitles(csvw):
    for i,table in enumerate(csvw['tables']):
        csvw['tables'][i]['tableSchema']['rowTitles'] = getTableTitles(table)['titles']
    return csvw
def getRowTitles(table):
    try:
        return table['tableSchema']['rowTitles']
    except:
        print('Falla GetRowTitles')
        sys.exit()
#Devuelve la URL de la tabla sobre la que estamos trabajando
def getUrl(table):
    try:
        if('url' in table.keys() and str(table['url']) not in emptyValues):
            getTableTitles(table)
            return str(table['url'])
        else:
            raise Exception("The format of CSVW is wrong, the Url is not valid")
    except Exception as e:
        print(e)
        sys.exit()

def getTableTitle(table):
    url = str(getUrl(table)).split("/")[-1:][0]
    return url
# Recorre la tabla en busca de los Titulos, pueden estar en el primer nivel del objeto Table (rowTiltles o rowTitle) tambien
# pueden estar dentro de las columnas de la tabla (table->tableSchema->columns[i]->title/s)
# TENER EN CUENTA LOS HEADERS --> SI ES TRUE ENTONCES LOS TITULOS YA ESTAN EN LA PRIMERA FILA!!!!
def getTableTitles(table):
    try:
        titles = []
        header = True

        if('dialect' in table.keys() and 'header' in table['dialect'].keys()):
            header =  table['dialect']['header']

        if('tableSchema' in table.keys()):
            if('rowTitles' in table['tableSchema'].keys() and len(table['tableSchema']['rowTitles']) > 0):
                titles = table['tableSchema']['rowTitles']
            elif('rowTitle' in table['tableSchema'].keys() and len(table['tableSchema']['rowTitle']) > 0):
                titles = table['tableSchema']['rowTitle']
        #print('TITLES:'  + str(titles))
        if(len(titles) == 0):
            #print("NO HAY ROW TITLES")
            #TODO BUSCAR LA FORMA DE MANEJAR LOS NOMBRES DE LOS CSVs
            path = './tmp/csv/' + str(table['url'].split("/")[-1:][0]) #.split('.')[0])
            try:
                delimiter = table['tableSchema']['dialect']['delimiter']
            except:
                delimiter = ','
            with open(path, "r") as f:
                reader = csv.reader(f)
                i = next(reader) 
                titles  = i
                if(delimiter != ','):
                    titles = i[0].split(delimiter)

        global rowTitles
        rowTitles = titles
        #print('ROWTITLES:' + str(rowTitles))
        #SI NO SE ESPECIFICA LOS ROWTITLES EN EL CSVW HAY QUE SACARLOS DEL CSV!!!!!!!
        return {'header':header, 'titles':titles}

    except Exception as e:
        print(e)
#Devuelve el array de titulos formateado listo para pasarselo directamente al BashScript
def getTitles(table):
    data = getTableTitles(table)
    titles = data['titles']
    result = ''.join(str(titles[i]) + ',' for i in range(0, len(titles)))
    result = result[:-1]
    return {'result':result, 'header':data['header']}

#Devuelve el delimitador, por defecto(Si no encuetra ningun delimitador en el csvw) es ',' 
def getDelimiter(table):
    try:
        result = {'delimiter':getDelimiterValue(table), 'arg':''}
#        result['arg'] = ''.join('$' + str(i) + ' ' for i in range(1, len(rowTitles) + 1))
        colsToPrint = []
        for i in table['filteredRowTitles']:
            colsToPrint.append(rowTitles.index(i)) 
        result['arg'] = ''.join('$' + str(i + 1) + '"\\",\\""' for i in sorted(colsToPrint))
        result['arg'] ='"\\""'+ result['arg'][:-6] + '\\""'
        return result
    except Exception as e:
        print(e)

#Devuelve el numero de filas que hay que saltarse por defecto es 0.
def getSkipRows(table):
    skipRows = 0
    if('dialect' in table.keys() and 'skipRows' in table['dialect'].keys()):
        skipRows = int(table['dialect']['skipRows'])
    return skipRows

#Recorre las columnas para almacenar el Null value en un ARRAY si no se encuntra ningun NUllvalue se usa el caracter vacio por defecto.
def getNullValues(table):
    nullValues  = [] 
    if(columnsChecker(table)):
        fullArg = ''
        result = {'data':[],'fullArg':''}
        for col in table['tableSchema']['columns']:
            title = getColTitle(col)
            index = rowTitles.index(title)
            if('null' in col.keys()):
                arg = 'gsub(/^%s$/,\"null\",$%s);'%(col['null'], str(index+1))
                result['data'].append({'col':'$%s'%(str(index+1)), 'value':col['null']})
                '''
                arg = ''
                if(index == 0):
                    arg = 'gsub(/^\\\"%s$/,\"\\\"null\",$1);'%(str(col['null']))
                elif(index > 0 and index < len(rowTitles) - 1):
                    arg = 'gsub(/^%s$/,\"null\",$%s);'%(col['null'], str(index+1))
                else:
                    arg =  'gsub(/^%s\\\"$/,\"null\\\"\",$%s);'%(col['null'], str(index+1))
                '''
                fullArg += arg
    result['fullArg'] = fullArg
    return result

#Get min and Max (Inclusive and exclusive)
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

#Devuelve el DataType->Format del DataType especificado
def getFormat(table, dataType):
    try:
        result = []
        if(columnsChecker(table)):
            for col in table['tableSchema']['columns']:
                title = getColTitle(col)
                indx = rowTitles.index(title)
                if('datatype' in col.keys()):
                    if( str(col['datatype']) == dataType and 'format' in col.keys()):
                        result.append({'col':str(indx + 1),'format':col['format']})
                    elif(type(col['datatype']) is dict and 'base' in col['datatype'] and 
                        'format' in col['datatype'] and col['datatype']['base'] == dataType):
                        result.append({'col':str(indx + 1), 'format':col['datatype']['format']})
        return result
    except Exception as e:
        print(e)

#Lee el Formato de la fecha y manda de la configuracion necesaria para ejecutar el bashScript dateFormatChanger.sh
def getDateFormat(table):
    data = getFormat(table, 'date')
    result = {'split':'', 'print':[]}
    for date in data:
        if(str(date['format']).lower() not in ["yyyy-mm-dd", "yyyymmdd"]):
            arrayFormat = ''
            if(str(date['format']).lower()[0] == 'y'):
                arrayFormat = 'date%s[1] \"-\" date%s[2] \"-\" date%s[3]'%(str(date['col']),str(date['col']),str(date['col']))
            elif(str(date['format']).lower()[0] == 'm'):
                arrayFormat = 'date%s[1] \"-\" date%s[2] \"-\" date%s[3]'%(str(date['col']),str(date['col']),str(date['col']))
            else:
                arrayFormat = 'date%s[1] \"-\" date%s[2] \"-\" date%s[3]'%(str(date['col']),str(date['col']),str(date['col']))
            if('.' in date['format']):
                date['delimiter'] = '.'
            elif('/' in date['format']):
                date['delimiter'] = '/'
            elif('-' in date['format']):
                date['delimiter'] = '-'
            result['print'].append({'col':'$%s'%(str(date['col'])),'data':'dateValue%s'%(str(date['col']))})
            result['split'] += 'if($%s != \"$%sNULL\")split($%s,date%s,\"%s\");dateValue%s=%s;if($%s == \"$%sNULL\")dateValue%s=\"null\";'%(str(date['col']), str(date['col']),str(date['col']),str(date['col']),str(date['delimiter']),str(date['col']), arrayFormat, str(date['col']),str(date['col']),str(date['col']))
        elif(str(date['format']).lower() == "yyyymmdd"):
            arrayFormat = 'date%s[1] date%s[2] date%s[3] date%s[4]\"-\" date%s[5] date%s[6] \"-\" date%s[7] date%s[8]'%(
                    str(date['col']), str(date['col']), str(date['col']), str(date['col']),
                    str(date['col']),str(date['col']),str(date['col']),str(date['col']))
            date['delimiter'] = ''
            result['print'].append({'col':'$%s'%(str(date['col'])),'data':'dateValue%s'%(str(date['col']))})
            #result['split'] += 'split($%s,date%s,\"%s\");'%(str(date['col']), str(date['col']),str(date['delimiter']))
            result['split'] += '{if($%s != \"$%sNULL\")split($%s,date%s,\"%s\");dateValue%s=%s;if($%s == \"$%sNULL\")dateValue%s=\"null\";}'%(str(date['col']), str(date['col']),str(date['col']),str(date['col']),str(date['delimiter']),str(date['col']), arrayFormat, str(date['col']),str(date['col']),str(date['col']))
           
    return result

#Lee el formato de los booleans y manda la informacion necesaria para ejecutar el BashScript booleanFormatChanger.sh
def getBooleanFormat(table):
    booleans = getFormat(table, 'boolean')
    fullArg = ''
    for col in booleans:
        arg = ''
        col['format'] =  str(col['format'])
        data = col['format'].split("|")
        arg = 'gsub(/%s/,"true",$%s);gsub(/%s/,"false",$%s);'%(str(data[0]), str(col['col']), str(data[1]), str(col['col']))
        fullArg += arg
    return fullArg

def getDefaultEmptyStringValue(table):
    result = []
    if(columnsChecker(table)):
        for index,col in enumerate(table['tableSchema']['columns']):
            if('default' in col.keys()):
                result.append({'col':str(index + 1), 'default':col['default']})
    return result
#Check if the table includes Columns
def columnsChecker(table):
    return 'tableSchema'in table.keys() and 'columns' in table['tableSchema'].keys() and type(table['tableSchema']['columns']) is list and len(table['tableSchema']['columns']) > 0

def getColTitle(col):
    title = ''
    if('titles' in col.keys()):
        if(type(col['titles']) is list and len(col['titles']) > 0):
            title = str(col['titles'][0])
        elif(str(col['titles']) not in emptyValues):
            title = str(col['titles'])
    elif('title' in col.keys()):
        if(type(col['title']) is list and len(col['title']) > 0):
            title = str(col['title'][0])
        elif(str(col['title']) not in emptyValues):
            title = col['title'] 
    return title

def getGsubPatterns(table):
    result = {'split': '', 'gsub':'', 'print':'', 'delimiter':''}
    date = getDateFormat(table) 
    delimiter = getDelimiter(table)
    result['split'] =  str(date['split'])
    nullValues = getNullValues(table)
    for col in nullValues['data']:
        result['split'] = result['split'].replace(str(col['col'])+'NULL',col['value'])
    script = nullValues['fullArg']
   # script += getDefaultStringValue(table)
    script += getBooleanFormat(table)
    result['gsub'] = str(script)
    for el in date['print']:
        delimiter['arg'] = delimiter['arg'].replace(el['col'],' ' +  el['data'] + ' ')
    result['print'] = delimiter['arg']
    result['delimiter'] = delimiter['delimiter'].encode('unicode-escape').decode('ascii')
    return result

def getIndexOfCol(col, table):
    print('SEARCHING:' + str(col) + '\nIN:' + str(rowTitles))
    title = getColTitle(col)
    return getRowTitles(table).index(title) 

def getSeparatorValue(col):
    try:
        return str(col['separator'].encode('unicode-escape').decode('ascii'))
    except:
        return 'NONE'

def hasSeparator(col):
    return getSeparatorValue(col) != 'NONE'
def getNullValue(table):
    try:
        nullValue = str(col['null'].encode('unicode-escape').decode('ascii'))
    except:
        nullValue = ''
    return nullValue
def getDataType(col):
    try:
        dataType = col['datatype']
    except:
        dataType = ''
    return dataType
def getDelimiterValue(table):
    try:
        delimiter = str(table['dialect']['delimiter'].encode('unicode-escape').decode('ascii'))
    except:
        delimiter = ','
    return delimiter
def getCols(table):
    cols = []
    if(columnsChecker(table)):
        cols = table['tableSchema']['columns']
    return cols
def getFilteredTitles(table):
    result = [];
    for title in table['filteredRowTitles']:
        result.append(rowTitles.index(title))
    result = sorted(result)
    for i,title in enumerate(result):
        result[i] = rowTitles[result[i]]

    result = '"' + ''.join(str(result[i]) + '","' for i in range(0, len(result)))
    result = result[:-2]
    return result
def getSeparatorScripts(table):
    result = {'columns':[], 'script':''}
    if(columnsChecker(table)):
        for col in table['tableSchema']['columns']:
            if(hasSeparator(col)):
                index = str(getIndexOfCol(col, table) + 1)
                name = str(getColTitle(col)) + '.csv'
                separator = str(getSeparatorValue(col))
                delimiter = str(getDelimiterValue(col))
                result['script'] += '''len%s=split($%s,data%s,\"%s\");n%s=\"\";for(i=1;i<=len%s;++i){n%s=n%s NR \"%s\" data%s[i];system(\"echo \" n%s \" >> tmp/csv/%s\");n%s=\"\"}$%s=NR;'''%(index,index,index,separator,index,index,index,index,delimiter,index,index,name,index, index)
                result['columns'].append('$' + str(index))
    return result
