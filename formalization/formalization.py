
import re
import os
from rdflib.plugins.sparql import *

def toSecondNormalForm(mapping, file, column, separator, query):
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
    pom = [["ex:"+column, "$(column)"]]

    mapping["mappings"][column] = {"source": source, "s": s, "po": pom}

def createJoin(predicate, column):
    join = {}
    parameters = [["str1", column], ["str2", "$(id)"]]
    join["p"] = predicate
    join["o"] = [{"mapping": column, "condition:": {"function": "equal", "parameters": parameters}}]
    return join

def dataTranslation(file, column, separator):
    #substitute the column by an index (1,2,3...)
    os.system("")
    #create a new file named column with id,[column] and separate the values based on the separator
    #for the separated values, the id is going to be the same
    os.system("")

def getPredicateAndObjectFromQuery(query,column,mapping):
    for tm in mapping["mappings"]:
        i = 0
        for pom in mapping["mappings"][tm]["po"]:
            if re.match("\\$\\("+column+"\\)", mapping["mappings"][tm]["po"][i][1]):
                predicate = mapping["mappings"][tm]["po"][i][0]
        i += 1

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