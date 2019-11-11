import csvwParser as parser
import os

#Function to call the bash Scripts files and send the scvw data.
def scriptCaller(data):
    url = parser.getUrl(data).split("/")[-1:][0]
    insertTitles(parser.getTitles(data), url)
    rowSkipper(parser.getSkipRows(data), url)
    replaceDelimiter(parser.getDelimiter(data), url)
##Insert the titles of 
def insertTitles(data, path):
    os.system('./bashScripts/insertTitles.sh %s %s'%(data, path))


#If the rowSkiper is bigger than 0 the function execute the BashScritp
def rowSkipper(data, path):
    if(int(data)> 0):
        os.system('./bashScripts/skipRows.sh %s %s'%(data, path))

def replaceDelimiter(data, path):
        print("Delimiter: " + str(data) + " File: " + str(path))
        os.system('./bashScripts/delimiterReplacer.sh %s %s'%(data, path))
def main():
    csvw = parser.jsonLoader('../mappings/bio2rdf.csvw.json')
#    parsedCsvw = csvwParser.jsonIterator(csvw)
    for table in csvw['tables']:
        scriptCaller(table)

main()
