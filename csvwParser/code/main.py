#!/bin/python3
import csvwParser as parser
import os

#Function to remove not required CSVs
def filterCsvw(csvw, files):
    for index,table in enumerate(csvw['tables']):
        if(table['url'][-1:][0] not in files):
            csvw['tables'].pop(index)
    return csvw

#Function to call the bash Scripts files and send the scvw data.
def scriptCaller(data):
    url = parser.getUrl(data).split("/")[-1:][0]
    url = url.split('.')[0]
    print("********************" + url + "***************************")
    insertTitles(parser.getTitles(data), url)
    print("InsertTitles Done")
    #rowSkipper(parser.getSkipRows(data), url)
    print("Skip Rows Done")
    replaceDelimiter(parser.getDelimiter(data), url)
    print("Replace Delimiter Done")
    dateFormatReplacer(parser.getDateFormat(data), url)
    print("DateFormat Changer Done")
    '''
    booleanFormatReplacer(parser.getBooleanFormat(data), url)
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
    os.system('bash ./bashScripts/delimiterReplacer.sh \'%s\' \'%s\' %s'%(delimiter,arg,path))

'''
Dates and booleans format (csvw:format -> sql formats)
'''
def dateFormatReplacer(data, path):
    try:
        if(len(data) > 0):
            print(data)
            for date in data:
#                print("%s %s %s %s"%(date['args'],date['col'],date['delimiter'], path))
                os.system('bash ./bashScripts/optimized/allInOneFile \'%s\' %s %s \'%s\' %s'%(date['args'],date['col'],date['delimiter'], date['arg2'], path))
    except:
        sys.exit()
def booleanFormatReplacer(data, path):
    print(data)
    
    for col in data:
        os.system('bash ./bashScripts/booleanFormatChanger.sh %s %s %s %s'%(col['true'], col['false'], col['col'], path))

def nullFormatChanger(data, path):
    for col in data:
        print("Col:%s Null:%s"%(col['col'], col['null']))
        os.system('bash ./bashScripts/nullFormatChanger.sh \'%s\' %s %s'%(col['null'], col['col'], path))
def defaultEmptyStringFormatChanger(data, path):
    for col in data:
#        print("Col:%s Null:%s"%(col['col'], col['default']))
        os.system('bash ./bashScripts/defaultEmptyStringReplacer.sh \'%s\' %s %s'%(col['default'], col['col'], path))

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

def main():
    csvw = parser.jsonLoader('../mappings/ncbigene.csvw.json')
#    parsedCsvw = csvwParser.jsonIterator(csvw) TO DO
#    csvw = filterCsvw(csvw, ['CSV1','CSV2']) TO DO
    for table in csvw['tables']:
        scriptCaller(table)
if __name__ == '__main__':
    main()
