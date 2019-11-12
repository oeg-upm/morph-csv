import csvwParser as parser
import os

#Function to call the bash Scripts files and send the scvw data.
def scriptCaller(data):
    url = parser.getUrl(data).split("/")[-1:][0]
    print("********************" + url + "***************************")
    insertTitles(parser.getTitles(data), url)
    rowSkipper(parser.getSkipRows(data), url)
    replaceDelimiter(parser.getDelimiter(data), url)
    dateFormatReplacer(parser.getDateFormat(data), url)

'''
Insert row titles (from csvw:rowTitles)
'''
##Insert the titles of 
def insertTitles(data, path):
    #print("Titles: " + data)
    #data=data.replace(" ", "")
    os.system('./bashScripts/insertTitles.sh \'%s\' %s'%(data, path))

'''
#Skip rows (csvw:skipRows → remove the first n rows)
'''
#If the skipRow is bigger than 0 the function execute the BashScritp
def rowSkipper(data, path):
    if(int(data)> 0):
        os.system('./bashScripts/skipRows.sh %s %s'%(data, path))

'''
#Delimiter (csvw:delimiter → change to comma)
'''
def replaceDelimiter(data, path):
    delimiter = str(data.encode('utf-8'))[1:]
    #print("Delimiter: " + delimiter + " File: " + path)
    os.system('./bashScripts/delimiterReplacer.sh %s %s'%(delimiter, path))

'''
Dates and booleans format (csvw:format → sql formats)
'''
def dateFormatReplacer(data, path):
    print(data)


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
    csvw = parser.jsonLoader('../mappings/bio2rdf.csvw.json')
#    parsedCsvw = csvwParser.jsonIterator(csvw)
    for table in csvw['tables']:
        scriptCaller(table)

main()
