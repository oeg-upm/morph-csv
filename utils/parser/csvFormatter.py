#!/bin/python3
import csvwParser as parser
import json
import os

#Function to remove not required CSVs
def selectionFormatter(selection):
    result = {}
    for tm in selection:
        result[selection[tm]['source']] = selection[tm]['columns']
    return result
def csvwFilter(csvw, selection):
    selection = selectionFormatter(selection)
    result = {'@context':csvw['@context'], 'tables':[]}
    for table in csvw['tables']:
        title = parser.getTableTitle(table)
        if(title in selection.keys()):
            table['filteredRowTitles'] = selection[title]
            result['tables'].append(table)
#            scriptCaller(table, selection[title]['columns'])
#           parser.setFilteredRowTitles(selection[title])
    return result
#Function to call the bash Scripts files and send the scvw data.
def scriptCaller(data):
    #TODO BUSCAR LA FORMA DE MANEJAR LOS NOMBRE DE LOS CSVs 
    url = parser.getUrl(data).split("/")[-1:][0]
    #url = url.split('.')[0]
    print("********************" + url + "***************************")
    data = parser.filterCols(data)
    print(str(data).replace('\'', '"'))
    insertTitles(parser.getTitles(data), url)
    print("InsertTitles Done")
    replaceCsvFormat(parser.getGsubPatterns(data), url)
    '''
    #rowSkipper(parser.getSkipRows(data), url)
    print("Skip Rows Done")
    replaceDelimiter(parser.getDelimiter(data), url)
    print("Replace Delimiter Done")
    dateFormatReplacer(parser.getDateFormat(data), url)
    print("DateFormat Changer Done")
    #booleanFormatReplacer(parser.getBooleanFormat(data), url)
    print("BooleanFormat Changer Done")
    nullFormatChanger(parser.getNullValues(data), url)
    print("NullFormat Changer Done")
    defaultEmptyStringFormatChanger(parser.getDefaultEmptyStringValue(data), url)
    '''
'''
Insert row titles (from csvw:rowTitles)
'''
def insertTitles(data, path):
    print("Titles: " + str(data['result']))
    print("Header: " + str(data['header']))
#    os.system('bash ./bashScripts/insertTitles.sh \'%s\' %s'%(data, path))

'''
#Skip rows (csvw:skipRows -> remove the first n rows)
'''
#If the skipRow is bigger than 0 the function execute the BashScritp
def rowSkipper(data, path):
    if(int(data)> 0):
        os.system('bash ./bashScripts/skipRows.sh %s %s'%(data, path))

'''
#Delimiter (csvw:delimiter -> change to comma)
'''
def replaceDelimiter(data, path):
    delimiter = data['delimiter'].encode('unicode-escape').decode('ascii')
    arg = str(data['arg'])
#    print("Delimiter: " + delimiter.encode('unicode-escape') + " File: " + path)
    if(delimiter != ','):
        os.system('bash ./bashScripts/delimiterReplacer.sh \'%s\' \'%s\' %s'%(delimiter,arg,path))

'''
Dates and booleans format (csvw:format -> sql formats)
'''
def dateFormatReplacer(data, path):
    try:
        if(len(data) > 0):
            for date in data:
                if(not date['correct']):
#                print("%s %s %s %s"%(date['args'],date['col'],date['delimiter'], path))
                    os.system('bash ./bashScripts/optimized/allInOneFile \'%s\' \'%s\' \'%s\' \'%s\' \'%s\''%(date['args'],date['col'],date['delimiter'], date['arg2'], path))
    except:
        sys.exit()
def booleanFormatReplacer(data, path):
    print(data)
    
    for col in data:
        os.system('bash ./bashScripts/booleanFormatChanger.sh %s %s %s %s'%(col['true'], col['false'], col['col'], path))

def nullFormatChanger(data, path):
    #METER PATTERN GSUB DESDE ARG1
    '''
    for col in data:
        print("Col:%s Null:%s"%(col['col'], col['null']))
    '''
    os.system('bash ./bashScripts/nullFormatChanger.sh \'%s\' %s'%(data, path))
def defaultEmptyStringFormatChanger(data, path):
    for col in data:
#        print("Col:%s Null:%s"%(col['col'], col['default']))
        os.system('bash ./bashScripts/defaultEmptyStringReplacer.sh \'%s\' %s %s'%(col['default'], col['col'], path))

def replaceCsvFormat(data, path):
#    print("FORMATTER: " + str(data))
    #arg += 'print ' + str(data['arg']) + ';'
    os.system('bash bashScripts/csvFormatter \'%s\' \'%s\' \'%s\' \'%s\' \'%s\''%(str(data['delimiter']), str(data['gsub']),str(data['print']),str(data['split']),str(path)))
'''
Validity max/minimum value (not correct -> null)
'''


'''
Identify the date cols and boolean cols
'''

'''
Default (csvw:default -> empty string by default value)
'''


'''
RML+FnO in object (new column apply the transformation functions)
'''

'''
RML+FnO in refObjectMap (new column apply transformation functions)
'''

def csvFormatter(csvSelection):
    csvw = parser.jsonLoader('../../csvwParser/mappings/ncbigene.csvw.json')
    csvw = csvwFilter(csvw, csvSelection)
#    print(str(csvw).replace('\'', '"'))
    for table in csvw['tables']:
        scriptCaller(table)
def main():
    selection = json.loads('{"gene": {"source": "gene_info.gz", "columns": ["Modification_date", "chromosome", "GeneID"]}}')
    csvFormatter(selection)
    '''
    csvw = parser.jsonLoader('../../csvwParser/mappings/ncbigene.csvw.json')
#    parsedCsvw = csvwParser.jsonIterator(csvw) TO DO
#    csvw = filterCsvw(csvw, ['CSV1','CSV2']) TO DO
    for table in csvw['tables']:
        scriptCaller(table)
    '''
if __name__ == '__main__':
    main()
