import sys
import json
import subprocess
import clean.csvFormatter as csvFormatter
import clean.csvwParser as csvwParser
import selection.resourcesFromSparql as resourcesFromSparql
import selection.yarrrml as yarrrml
import formalization.formalization as formalizer
import schema_generation.from_mapping_to_sql as mapping2Sql
import schema_generation.create_and_insert as insert
import schema_generation.morph_properties as genproperties
import utils.utilsresources as utils
def runTest(csvwPath, mappingPath, queryPath,expectedResults):
	print('Testing Query: '  + queryPath)
	csvw = json.loads(open(csvwPath).read())
	csvw = csvwParser.insertRowTitles(csvw)
	sparqlQuery = utils.readQuery(queryPath)
	utils.sparqlQueryParser(queryPath)
	parsedQuery = json.loads(open('tmp/annotations/sparql.json').read())
	#Extracting the functions from the mapping:
	functions, mapping = yarrrml.getCleanYarrrml(mappingPath)
	csvColumns, mapping = resourcesFromSparql.fromSPARQLtoMapping(mapping, sparqlQuery, parsedQuery)
	csvColumns, functions = resourcesFromSparql.getColumnsFromFunctions(csvColumns, functions)
	checkColumns(csvColumns, expectedResults['csvColumns'])
	csvw = csvFormatter.csvwFilter(csvw, csvColumns)
	print('The Required Elements are correct')
	formalizedData = formalizer.addNormalizedTablesToCsvw(csvw, mapping, sparqlQuery, parsedQuery)
	csvw = formalizedData['csvw']
	query = formalizedData['query']
	mapping = formalizedData['mapping']
	csvFormatter.csvFormatter(csvw)
	print(str(csvw).replace('\'', '"'))
	#Checking the format:
	checkFormat(csvw, expectedResults['format'])
	print('The format is correct')
	yarrrml.fromSourceToTables(mapping)
	schema = mapping2Sql.generate_sql_schema(csvw, 
			functions, 
			mapping2Sql.decide_schema_based_on_query(mapping))
	checkSchema(schema, expectedResults['schema'])
	print('The Schema is Correct')

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

def checkFormat(csvw, result):
	try:
		for table in csvw['tables']:
			path = 'tmp/csv/' + csvwParser.getUrl(table).split("/")[-1:][0]
			with open(path, "r") as f:
				data = ''.join(f.readline() for i in range(2))
			if(data != result):
				raise Exception('The Format is wrong: ' + path)
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


def main():
	testConfig = json.loads(open('test/testConfig.json').read())
	for dataset in testConfig:
		for query in testConfig[dataset]["queries"]:
			queryPath = testConfig[dataset]["queriesPath"] + str(query["name"])
			csvwPath = testConfig[dataset]["csvwPath"]
			mappingPath = testConfig[dataset]["mappingPath"]
			expectedResult = query
			runTest(csvwPath, mappingPath, queryPath, expectedResult)
if __name__ == '__main__':
	main()
