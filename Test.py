import argparse
import sys
import json
import subprocess
import clean.csvFormatter as csvFormatter
import clean.csvwParser as csvwParser
import selection.resourcesFromSparql as resourcesFromSparql
import selection.yarrrml as yarrrml
import normalization.normalization as normalizer
import schema_generation.from_mapping_to_sql as mapping2Sql
import schema_generation.create_and_insert as insert
import schema_generation.morph_properties as genproperties
import utils.utilsresources as utils
import schema_generation.create_and_insert as insert
import schema_generation.creation_sql_alters as sqlAlters

def runTest(csvwPath, mappingPath, queryPath,expectedResults):
	print('Testing Query: '  + queryPath)
	csvw = json.loads(open(csvwPath).read())
	csvw = csvwParser.insertRowTitles(csvw)
	sparqlQuery = utils.readQuery(queryPath)
	print(sparqlQuery)
	utils.sparqlQueryParser(queryPath)
	parsedQuery = json.loads(open('tmp/annotations/sparql.json').read())
	#Extracting the functions from the mapping:
	functions, mapping = yarrrml.getCleanYarrrml(mappingPath)
	csvColumns, mapping = resourcesFromSparql.fromSPARQLtoMapping(mapping, sparqlQuery, parsedQuery)
	csvColumns, functions = resourcesFromSparql.getColumnsFromFunctions(csvColumns, functions)
	checkColumns(csvColumns, expectedResults['csvColumns'])
	csvw = csvFormatter.csvwFilter(csvw, csvColumns)
	print('The Required Elements are correct')
	normalizedData = normalizer.addNormalizedTablesToCsvw(csvw, mapping, sparqlQuery, parsedQuery)
	csvw = normalizedData['csvw']
	query = normalizedData['query']
	mapping = normalizedData['mapping']
	csvFormatter.csvFormatter(csvw)
	print(str(csvw).replace('\'', '"'))
	#Checking the format:
	checkFormat(csvw, expectedResults['format'])
	print('The format is correct')
	yarrrml.fromSourceToTables(mapping)
	schema,alters = mapping2Sql.generate_sql_schema(csvw,
                        mapping,
			mapping2Sql.decide_schema_based_on_query(mapping))
	checkSchema(schema, expectedResults['schema'])
	print('The Schema is Correct')

def generateData(csvwPath, mappingPath, queryPath):
	csvw = json.loads(open(csvwPath).read())
	csvw = csvwParser.insertRowTitles(csvw)
	sparqlQuery = utils.readQuery(queryPath)
	utils.sparqlQueryParser(queryPath)
	parsedQuery = json.loads(open('tmp/annotations/sparql.json').read())
	functions, mapping = yarrrml.getCleanYarrrml(mappingPath)
	csvColumns, mapping = resourcesFromSparql.fromSPARQLtoMapping(mapping, sparqlQuery, parsedQuery)
	print(str(csvColumns).replace('}', '}\n'))
	csvColumns, functions = resourcesFromSparql.getColumnsFromFunctions(csvColumns, functions)
	#print(str(mapping).replace('\'', '"').replace('True', 'true').replace('False', 'false'))
	#print(str(csvColumns).replace('\'', '"').replace('True', 'true').replace('False', 'false'))
	csvw = csvFormatter.csvwFilter(csvw, csvColumns)
	normalizedData = normalizer.addNormalizedTablesToCsvw(csvw, mapping, sparqlQuery, parsedQuery)
	csvw = normalizedData['csvw']
	query = normalizedData['query']
	mapping = normalizedData['mapping']
	csvFormatter.csvFormatter(csvw)
	yarrrml.fromSourceToTables(mapping)
	schema,alters = mapping2Sql.generate_sql_schema(csvw,
                        mapping,
			mapping2Sql.decide_schema_based_on_query(mapping))
	sqlFunctions = sqlAlters.translate_fno_to_sql(functions)
	try:
		insert.create_and_insert(csvw, schema, sqlFunctions, alters)
	except Exception as e:
                print('HA FALLADO')
                print(e)
                sys.exit()
	print('csvColumns:\n' + str(csvColumns).replace("'",'"').replace('}', '}\n') + '\n\n*****************************\n\n')
	print('CSV Format:\n' + str(readFormat(csvw)).replace("'", '"') + '\n\n*****************************\n\n')
	print('SQL Schema:\n' + str(schema).replace(';', ';\n') + str(alters).replace(';', ';\n'))
	if(len(str(sqlFunctions)) > 0):
		print(str(sqlFunctions).replace(';', ';\n') + '\n\n*****************************\n\n')



def checkColumns(columns, result):
	#{TmName:{sourceName:[colName]}}
	try:
		for tm in result:
			if(tm not in columns.keys()):
				raise Exception('Error, in TM: ' + tm)
			if('source' not in columns[tm].keys() or columns[tm]['source'] != result[tm]['source']):
				raise Exception('Error in Sources: ' + tm +  ' ' + source)
			for col in result[tm]['columns']:
				if(col not in columns[tm]['columns']):
					raise Exception('Error in Columns: ' + tm + ' ' + source + ' ' + col)
	except Exception as e:
		print(e)
		sys.exit()
def readFormat(csvw):
	result = {}
	for table in csvw['tables']:
		path = 'tmp/csv/' + csvwParser.getUrl(table).split("/")[-1:][0]
		with open(path, "r") as f:
			result[path] =  ''.join(f.readline() for i in range(2))
	return result
def checkFormat(csvw, result):
	try:
		data = readFormat(csvw)
		for table in result:
			if(data[table] != result[table]):
				raise Exception('The Format is wrong: ' + table)
	except Exception as e:
		print('Falla CheckFormat')
		print(e)
		sys.exit()

def checkSchema(schema, result):
	try:
		if(schema != result):
			raise Exception('The Schema is wrong: \n' + schema)
	except Exception as e:
		print('Falla checkSchema')
		print(e)
		sys.exit()

'''
def main():
	testConfig = json.loads(open('test/testConfig.json').read())
	for dataset in testConfig:
		for query in testConfig[dataset]["queries"]:
			queryPath = testConfig[dataset]["queriesPath"] + str(query["name"])
			csvwPath = testConfig[dataset]["csvwPath"]
			mappingPath = testConfig[dataset]["mappingPath"]
			expectedResult = query
			#runTest(csvwPath, mappingPath, queryPath, expectedResult)
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--json_config", required=True, help="Input config file with yarrrml and csvw")
    parser.add_argument("-q", "--sparql_query", required=True, help="SPARQL query")
    args = parser.parse_args()
    if len(sys.argv) == 5:
        try:
            with open(args.json_config, "r") as json_file:
                config = json.load(json_file)
            queryPath = str(args.sparql_query)

        except ValueError:
            print("No input the correct arguments, run pip3 morphcsv.py -h to see the help")
            sys.exit()
    else:
        print("No input the correct arguments, run pip3 morphcsv.py -h to see the help)")
        sys.exit()

    utils.maketmpdirs()
    generateData('tmp/annotations/annotations.json','tmp/annotations/mapping.yaml',queryPath)

if __name__ == '__main__':
	main()
