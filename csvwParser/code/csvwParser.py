#!/bin/python3
import json
import sys
import os
import csv

#Valores nulos que se usan para verificar la validez de los datos.
emptyValues = ['', ' ']
rowTitles = []
#Carga el CSVW en el DataFrame
def jsonLoader(path):
    try:
        result = json.loads(str(open(path).read()))
        return result
    except Exception as e:
        print(e)
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

# Recorre la tabla en busca de los Titulos, pueden estar en el primer nivel del objeto Table (rowTiltles o rowTitle) tambien
# pueden estar dentro de las columnas de la tabla (table->tableSchema->columns[i]->title/s)
# TENER EN CUENTA LOS HEADERS --> SI ES TRUE ENTONCES LOS TITULOS YA ESTAN EN LA PRIMERA FILA!!!!
def getTableTitles(table):
    try:
        titles = []
        header = False
        if('dialect' in table.keys() and 'header' in table['dialect'].keys()):
            header =  table['dialect']['header']
        if('tableSchema' in table.keys()):
            if('rowTitles' in table['tableSchema'].keys() and len(table['tableSchema']['rowTitles']) > 0):
                titles = table['tableSchema']['rowTitles']
            elif('rowTitle' in table['tableSchema'].keys() and len(table['tableSchema']['rowTitle']) > 0):
                titles = table['tableSchema']['rowTitle']
        if(header is True and len(titles) == 0):
            path = './tmp/' + str(table['url'].split("/")[-1:][0].split(".")[0])
            delimiter = getDelimiter(table)['delimiter']
            with open(path, "r") as f:
                reader = csv.reader(f)
                i = next(reader) 
                titles = i[0].split(delimiter)
        global rowTitles
        rowTitles = titles
        #SI NO SE ESPECIFICA LOS ROWTITLES EN EL CSVW HAY QUE SACARLOS DEL CSV!!!!!!!
        return {'header':header, 'titles':titles}

    except Exception as e:
        print(e)
        pass
    
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
        result = {'delimiter':',', 'arg':''}
        if('dialect' in table.keys() and type(table['dialect']) is dict and 'delimiter' in table['dialect'].keys() and str(table['dialect']['delimiter']) != ''):
           result['delimiter'] = table['dialect']['delimiter']
        result['arg'] = ''.join('$' + str(i) + '"\\",\\""' for i in range(1, len(rowTitles) + 1))
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
        for col in table['tableSchema']['columns']:
            title = getColTitle(col)
            index = rowTitles.index(title)
            if('null' in col.keys()):
                nullValues.append({'col':str(index +1), 'null':col['null']})
            else:
                nullValues.append({'col':str(index + 1), 'null':''})
    return nullValues

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
    dates = getFormat(table, 'date')
    for date in dates:
        if(str(date['format']).lower()[0] == 'y'):
            date['args'] = '$3\"-\"$2\"-\"$1'#Hace referencia a las columnas que tiene que reordenar AWK tras dividir la columna 'col' segun el delimitador dado
        elif(str(date['format']).lower()[0] == 'm'):
            date['args'] =  '$3\"-\"$1\"-\"$2'
        else:
            date['args'] = '$3\"-\"$2\"-\"$1'
        if('.' in date['format']):
            date['delimiter'] = '.'
        elif('/' in date['format']):
            date['delimiter'] = '/'
        elif('-' in date['format']):
            date['delimiter'] = '-'
        else:
            date['delimiter'] = 'none'
        date['arg2'] = ''.join('$' + str(i)  + '"\\",\\""' for i in range(1, len(rowTitles) + 1))
        date['arg2'] = str(date['arg2']).replace("$"+ str(date['col']) +  '"\\",\\""', 'f1' +  '"\\",\\""')
        date['arg2'] = date['arg2'][:-7]
    return dates

#Lee el formato de los booleans y manda la informacion necesaria para ejecutar el BashScript booleanFormatChanger.sh
def getBooleanFormat(table):
    booleans = getFormat(table, 'boolean')
    for col in booleans:
        col['format'] =  str(col['format'])
        data = col['format'].split("|")
        col['true'] = str(data[0])
        col['false'] = str(data[1])

    return booleans

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
        if( (isinstance(col['titles'], str) or isinstance(col['titles'], unicode)) and str(col['titles']) not in emptyValues):
            title = str(col['titles'])
        elif(type(col['titles']) is list and len(col['titles']) > 0):
            titles = str(col['titles'][0])
    elif('title' in col.keys()):
        if((isinstance(col['title'], str) or isinstance(col['title'], unicode)) and str(col['title']) not in emptyValues):
            title = str(col['title'])
        elif(type(col['title']) is list and len(col['title']) > 0):
            title = str(col['title'][0])
    return title
