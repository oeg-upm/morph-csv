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

##Insert the titles of 
def insertTitles(data, path):
    #print("Titles: " + data)
    #data=data.replace(" ", "")
    os.system('./bashScripts/insertTitles.sh \'%s\' %s'%(data, path))


#If the skipRow is bigger than 0 the function execute the BashScritp
def rowSkipper(data, path):
    if(int(data)> 0):
        os.system('./bashScripts/skipRows.sh %s %s'%(data, path))

def replaceDelimiter(data, path):
    delimiter = str(data.encode('utf-8'))[1:]
    #print("Delimiter: " + delimiter + " File: " + path)
    os.system('./bashScripts/delimiterReplacer.sh %s %s'%(delimiter, path))

def dateFormatReplacer(data, path):
    print(data)
def main():
    csvw = parser.jsonLoader('../mappings/bio2rdf.csvw.json')
#    parsedCsvw = csvwParser.jsonIterator(csvw)
    for table in csvw['tables']:
        scriptCaller(table)

main()
