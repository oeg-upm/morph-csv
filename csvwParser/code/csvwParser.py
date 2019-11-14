#!/bin/python3
import json
import sys
import os

#Valores nulos que se usan para verificar la validez de los datos.
emptyValues = ['', ' ']

#Carga el CSVW en el DataFrame
def jsonLoader(path):
    try:
        result = json.loads(open(path).read())
        return result
    except Exception as e:
        print(e)
        print("The path is not valid")
        sys.exit()

#Devuelve la URL de la tabla sobre la que estamos trabajando
def getUrl(table):
    try:
        if('url' in table.keys() and str(table['url']) not in emptyValues):
            return str(table['url'])
        else:
            raise Exception("The format of CSVW is wrong, the Url is not valid")
    except Exception as e:
        print(e)
        sys.exit()

#Recorre la tabla en busca de los Titulos, pueden estar en el primer nivel del objeto Table (rowTiltles o rowTitle) tambien
# pueden estar dentro de las columnas de la tabla (table->tableSchema->columns[i]->title/s)
def getTableTitles(table):
    try:
        titles = []
        if('rowTitles' in table.keys() and len(table['rowTitles']) > 0):
            titles = table['rowTitles']
        elif('rowTitle' in table.keys() and len(table['rowTitle']) > 0):
            titles = table['rowTitle']
        elif(columnsChecker(table)):
            for col in table['tableSchema']['columns']:
                if('titles' in col.keys()):
                    if( (isinstance(col['titles'], str) or isinstance(col['titles'], unicode)) and str(col['titles']) not in emptyValues):
                        titles.append(str(col['titles']))
                    elif(type(col['titles']) is list and len(col['titles']) > 0):
                        titles = titles + col['titles']
                elif('title' in col.keys()):
                    if((isinstance(col['title'], str) or isinstance(col['title'], unicode)) and str(col['title']) not in emptyValues):
                        titles.append(str(col['title']))
                    elif(type(col['title']) is list and len(col['title']) > 0):
                        titles = titles + col['title']
        return titles

    except Exception as e:
        print(e)
        pass
    
#Devuelve el array de titulos formateado listo para pasarselo directamente al BashScript
def getTitles(table):
    titles = getTableTitles(table)
    result = ''.join(str(titles[i]) + ',' for i in range(0, len(titles)))
    result = result[:-1]
    return result

#Devuelve el delimitador, por defecto(Si no encuetra ningun delimitador en el csvw) es ',' 
def getDelimiter(table):
    try:
        delimiter = ','
        if('dialect' in table.keys() and type(table['dialect']) is dict and 'delimiter' in table['dialect'].keys() and str(table['dialect']['delimiter']) != ''):
            delimiter = str(table['dialect']['delimiter'])
        return delimiter
    except Exception as e:
        print(e)

#Devuelve el numero de filas que hay que saltarse por defecto es 0.
def getSkipRows(table):
    skipRows = 0
    if('dialect' in table.keys() and 'skipRows' in table['dialect'].keys()):
        skipRows = int(table['dialect']['skipRows'])
    return skipRows

#Recorre las columnas para almacenar el Null value en un ARRAY si no se encuntra ningun NUllvalue se usa el caracter vacio por defecto.
def getNullValue(table):
    nullValues  = [] 
    if(columnsChecker(table)):
        for index, col in enumerate(table['tableSchema']['columns']):
            if('null' in col.keys()):
                nullValues.append({'col':str(index +1), 'null':col['null']})
            else:
                nullValues.append('col':str(index + 1), 'null':'')
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
            for indx, col in enumerate(table['tableSchema']['columns']):
                if('datatype' in col.keys()):
                    if((isinstance(col['datatype'], str) or isinstance(col['datatype'], unicode)) and col['datatype'] == dataType and 'format' in col.keys()):
                        result.append({'col':indx,'format':col['format']})
                    elif(type(col['datatype']) is dict and 'base' in col['datatype'] and 'format' in col['datatype'] and col['datatype']['base'] == dataType):
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

#Check if the table includes Columns
def columnsChecker(table):
    return 'tableSchema'in table.keys() and 'columns' in table['tableSchema'].keys() and type(table['tableSchema']['columns']) is list and len(table['tableSchema']['columns']) > 0


