parser = __import__('./code/csvwParser')

def main():
    csvw = parser.jsonLoader('./mappings/bio2rdf.csvw.json')
    parsedCsvw = parser.jsonIterator(csvw)

if __name__ == '__init__':
    main()
