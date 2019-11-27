
import re
import os
from rdflib.plugins.sparql import *
def addNormalizedTableToCsvw(csvw):
    a=0
    #for table in csvw['table']:
        
def toSecondNormalForm(mapping, file, column, separator, query):
    #Requirements for NORMALIZATION: csvw, yarrrmlMapping, sparqlQuery.
    mappingTranslation(mapping, column)
    dataTranslation(file, column, separator)
    queryRewritten(query, getPredicateAndObjectFromQuery(query, column, mapping), column)

def queryRewritten(query, predicate, variable, column):
    re.sub(predicate + "\\s+" + variable, "?"+column+" . ?"+column+" ex:"+column+" ?"+variable, query)

def mappingTranslation(mapping, column):
    for tm in mapping["mappings"]:
        i = 0
        for pom in mapping["mappings"][tm]["po"]:
            if re.match("\\$\\("+column+"\\)", mapping["mappings"][tm]["po"][i][1]):
                mapping["mappings"][tm]["po"][i] = createJoin(mapping["mappings"][tm]["po"][i][0], column)
        i += 1

    source = [["./tmp/csv/"+column.csv]]
    s = "http://example.com/$(id)-$("+column+")"
    pom = [["ex:"+column, "$(value)"]]

    mapping["mappings"][column] = {"source": source, "s": s, "po": pom}

def createJoin(predicate, column):
    join = {}
    parameters = [["str1", column], ["str2", "$(id)"]]
    join["p"] = predicate
    join["o"] = [{"mapping": column, "condition:": {"function": "equal", "parameters": parameters}}]
    return join

def dataTranslation(file, column, separator):
    #ToDo call the bash scripts
    #substitute the column by an index (1,2,3...)
    os.system("")
    #create a new file named column with id,[column] and separate the values based on the separator
    #for the separated values, the id is going to be the same
    os.system("")

def getPredicateAndObjectFromQuery(query,column,mapping):
    for tm in mapping["mappings"]:
        i = 0
        for i,pom in enumerate(mapping["mappings"][tm]["po"]):
            if re.match("\\$\\("+column+"\\)", mapping["mappings"][tm]["po"][i][1]):
                predicate = mapping["mappings"][tm]["po"][i][0]

    algebra = prepareQuery(query).algebra
    for bgp in algebra['p']['p']:
        if bgp == "triples":
            for tp in algebra['p']['p']['triples']:
                if re.match(predicate,algebra['p']['p']['triples'][tp][1]):
                    object = algebra['p']['p']['triples'][tp][2]
        elif re.match("p[0-9]*", bgp):
                for tp in algebra['p']['p'][bgp]['triples']:
                    if re.match(predicate, algebra['p']['p'][bgp]['triples'][tp][1]):
                        object = algebra['p']['p'][bgp]['triples'][tp][2]

    return predicate, object

def toThirdNormalForm(mapping):

    equal = {}
    normalize = []
    for tm in mapping["mappings"]:
        for pom in mapping["mappings"][tm]["po"]:
            if 'p' in pom:
                source = mapping["mappings"][tm]["sources"][0][0]
                parent_mapping = mapping["mappings"][tm]["po"]["o"]["mapping"]
                source_parent = mapping["mappings"][parent_mapping]["sources"][0][0]
                if source == source_parent:
                    for i in range(len(mapping["mappings"][tm]["po"]["o"]["condition"]["parameters"])):
                        if mapping["mappings"][tm]["po"]["o"]["condition"]["parameters"][i][0] == "str2":
                            reference = getColumnsfromOM(mapping["mappings"][tm]["po"]["o"]["condition"]["parameters"][i][1])
                            equal[parent_mapping] = reference[0]

    for tm in equal:
        target = tm
        source = mapping["mappings"][tm]["sources"][0][0]
        columns = []
        pomcount = 0
        for pom in mapping["mappings"][tm]["pom"]:
            if 'p' in pom:
                columns.extend(getColumnsfromJoin(mapping["mappings"][tm]["po"][pomcount]["o"]))
            else:
                columns.extend(getColumnsfromOM(mapping["mappings"][tm]["po"][pomcount][1]))
            pomcount += 1

        remove = columns.copy().pop(equal[tm])
        mapping["mappings"][tm]["sources"][0][0] = "./tmp/csv/"+target+".csv~csv"
        normalize.extend({"source": source, "remove": remove, "columns": columns, "target": target})

    """
        normalize content:
            - source: the name of the file where you can get the columns
            - remove: the columns you have to remove from source
            - target: the name of the new file
            - columns: the columns you have to add to target
        
    """
    # ToDo: execute bash script to create target and remove the "remove" columns from source



def getColumnsfromOM(om):
    columns = []
    aux = om.split("$(")
    for references in aux:
        if re.match(".*\\).*", references):
            columns.append(references.split(")")[0])
    return columns

def getColumnsfromJoin(join):
    columns = []
    joinscount = 0
    while joinscount < len(join):
        for i in [0, 1]:
            if join[joinscount]["condition"]["parameters"][i][0] == "str1":
                columns.extend(getColumnsfromOM(join[joinscount]["condition"]["parameters"][i][1]))
        joinscount += 1
    return columns
