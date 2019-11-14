import csvwParser as parser
import os

#Function to call the bash Scripts files and send the scvw data.
def scriptCaller(data):
    url = parser.getUrl(data).split("/")[-1:][0]
    print("********************" + url + "***************************")
    insertTitles(parser.getTitles(data), url)
    print("InsertTitles Done")
    rowSkipper(parser.getSkipRows(data), url)
    print("Skip Rows Done")
    replaceDelimiter(parser.getDelimiter(data), url)
    print("Replace Delimiter Done")
    dateFormatReplacer(parser.getDateFormat(data), url)
<<<<<<< HEAD
    print("DateFormat Changer Done")
    booleanFormatReplacer(parser.getBooleanFormat(data), url)
=======

'''
Insert row titles (from csvw:rowTitles)
'''
>>>>>>> b9bbfa9b251f574f4604a9b9e1d20f7a42bbe950
##Insert the titles of 
def insertTitles(data, path):
#    print("Titles: " + data)
    os.system('bash ./bashScripts/insertTitles.sh \'%s\' %s'%(data, path))

'''
#Skip rows (csvw:skipRows → remove the first n rows)
'''
#If the skipRow is bigger than 0 the function execute the BashScritp
def rowSkipper(data, path):
    if(int(data)> 0):
        os.system('bash ./bashScripts/skipRows.sh %s %s'%(data, path))

'''
#Delimiter (csvw:delimiter → change to comma)
'''
def replaceDelimiter(data, path):
    delimiter = str(data.encode('utf-8'))
    #print("Delimiter: " + delimiter + " File: " + path)
    os.system('bash ./bashScripts/delimiterReplacer.sh \'%s\' %s'%(delimiter, path))

'''
Dates and booleans format (csvw:format → sql formats)
'''
def dateFormatReplacer(data, path):
    if(len(data) > 0):
        for date in data:
  #          print("%s %s %s %s"%(date['args'],date['col'],date['delimiter'], path))
            os.system('bash ./bashScripts/dateFormatChanger.sh \'%s\' %s %s %s'%(date['args'],date['col'],date['delimiter'], path))
def booleanFormatReplacer(data, path):
    print(data)
    '''
    for col in data:
        os.system('bash ./bashScripts/booleanFormatChanger.sh %s %s %s %s'%(data['col'], data['true'], data['false'], path))
    '''

'''
Validity max/minimum value (not correct → null)
'''


'''
Identify the date cols and boolean cols
'''

'''
Default (csvw:default → empty string by default value)
'''


'''
RML+FnO in object (new column apply the transformation functions)
'''

'''
RML+FnO in refObjectMap (new column apply transformation functions)
'''

def main():
    csvw = parser.jsonLoader('../mappings/madridGtfs.csvw.json')
#    parsedCsvw = csvwParser.jsonIterator(csvw)
#    csvw = filterCsvw(csvw, ['CSV1','CSV2'])
    for table in csvw['tables']:
        scriptCaller(table)

main()

