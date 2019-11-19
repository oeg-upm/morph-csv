import rdflib
from rdflib.plugins.sparql import *
import re
import yaml
import copy


def fromSPARQLtoMapping(mapping, query):
    query = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>" \
            "PREFIX schema: <http://schema.org/> " \
            "select * where { ?s rdf:type schema:SocialMediaPosting ." \
            "?s schema:author ?author . " \
            "?p rdf:type schema:Person ." \
            "?p schema:name ?name ." \
            "?p schema:familyName ?name2 .}"
    algebra = prepareQuery(query).algebra
    uris = {}
    for bgp in algebra['p']['p']:
        if bgp == "triples":
            for tp in algebra['p']['p']['triples']:
                obtainURISfromTP(tp, uris)
        elif re.match("p[0-9]*", bgp):
            for tp in algebra['p']['p'][bgp]['triples']:
                obtainURISfromTP(tp, uris)
    translatedmap, csvColumns = getRelevantTM(uris, mapping)
    f = open("./tmp/mapping_aux.yml", "w+")
    f.write(yaml.dump(translatedmap, default_flow_style=None))
    f.close()
    # call("../bash/yarrrml-parser.sh", shell=True)
    return csvColumns


def obtainURISfromTP(tp, uris):
    if str(tp[0]) not in uris.keys():
        uris[str(tp[0])] = {"predicates": [], "types": []}
    for value in tp:
        if re.match(".*URIRef.*", str(type(value))):
            if str(value) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
                uris[str(tp[0])]["types"].append(str(tp[2]))
            elif str(tp[1]) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and value == tp[1]:
                uris[str(tp[0])]["predicates"].append(str(value))


def getRelevantTM(uris, mapping):
    mapping = substitutePrefixes(mapping)
    relevantTM = {}
    csvColumns = {}
    parentcolumns = {}
    for subject in uris:
        lensubject = len(uris[subject]["predicates"]) + len(uris[subject]["types"])
        predicates = uris[subject]["predicates"]
        types = uris[subject]["types"]
        for tm in mapping["mappings"]:
            pomcount = 0
            equals = 0
            relevantpos = []
            columns = []
            for pom in mapping["mappings"][tm]["po"]:
                if 'p' in pom:
                    if mapping["mappings"][tm]["po"][pomcount]["p"] in predicates:
                        equals += 1
                        relevantpos.append(pomcount)
                        aux, auxparentcolumns, parent = getColumnsfromJoin(mapping["mappings"][tm]["po"][pomcount]["o"])
                        parentcolumns[parent] = auxparentcolumns
                        columns.extend(aux)
                elif mapping["mappings"][tm]["po"][pomcount][0] in predicates:
                    equals += 1
                    relevantpos.append(pomcount)
                    columns.extend(getColumnsfromOM(mapping["mappings"][tm]["po"][pomcount][1]))
                elif mapping["mappings"][tm]["po"][pomcount][0] == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
                    if mapping["mappings"][tm]["po"][pomcount][1] in types:
                        equals += 1
                        relevantpos.append(pomcount)
                pomcount += 1
            if lensubject == equals:
                source = re.sub("~csv", "", mapping["mappings"][tm]["sources"][0][0].split("/")[
                    len(mapping["mappings"][tm]["sources"][0][0].split("/")) - 1])
                columns.extend(getColumnsfromOM(mapping["mappings"][tm]["s"]))
                columns = list(dict.fromkeys(columns))
                relevantTM[tm] = relevantpos
                csvColumns[tm] = {"source": source, "columns": columns}
                break

    for parent in parentcolumns:
        for tm in csvColumns:
            if parent in csvColumns[tm]:
                csvColumns[tm]["columns"].extend(parentcolumns[parent])
                csvColumns[tm]["columns"] = list(dict.fromkeys(csvColumns["columns"][parent]))

    mappingcopy = copy.deepcopy(mapping["mappings"])
    for tm in mappingcopy:
        if tm not in relevantTM:
            del mapping["mappings"][tm]
        else:
            pomcount = 0
            while pomcount < len(mapping["mappings"][tm]["po"]):
                if pomcount not in relevantTM[tm]:
                    del mapping["mappings"][tm]["po"][pomcount]
                    count = 0
                    for x in relevantTM[tm]:
                        if x >= pomcount:
                            relevantTM[tm][count] = x - 1
                        count += 1
                else:
                    pomcount += 1

    return mapping, csvColumns


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
            else:
                parentColumns = getColumnsfromOM(join[joinscount]["condition"]["parameters"][i][1])
                parent = join[joinscount]["mapping"]
        joinscount += 1
    return columns, parentColumns, parent


def substitutePrefixes(mapping):
    prefixes = mapping["prefixes"]

    for tm in mapping["mappings"]:
        pomcount = 0
        for pom in mapping["mappings"][tm]["po"]:
            if 'p' in pom:
                value = mapping["mappings"][tm]["po"][pomcount]["p"]
                join = True
            else:
                value = mapping["mappings"][tm]["po"][pomcount][0]
                join = False
            if re.match(".*:.*", value):
                aux = atomicprefixsubtitution(prefixes, value)
                if join:
                    mapping["mappings"][tm]["po"][pomcount]["p"] = aux[0] + aux[1]
                else:
                    mapping["mappings"][tm]["po"][pomcount][0] = aux[0] + aux[1]
            elif "a" == value:
                mapping["mappings"][tm]["po"][pomcount][0] = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
                aux = atomicprefixsubtitution(prefixes, mapping["mappings"][tm]["po"][pomcount][1])
                mapping["mappings"][tm]["po"][pomcount][1] = aux[0] + aux[1]
            pomcount += 1
    return mapping


def atomicprefixsubtitution(prefixes, value):
    aux = value.split(":")
    for prefix in prefixes.keys():
        if aux[0] == prefix:
            aux[0] = prefixes[prefix]
            break
    return aux


def getColumnsFromFunctions(csvColumns, functions):
    for tm in functions:
        for csv in csvColumns:
            sourceColumns = csvColumns[tm]["columns"]
            for column in sourceColumns:
                if column in functions[tm]:
                    columns = []
                    extractReferencesFromFno(functions[tm][column], columns)
                    csvColumns[tm]["columns"].remove(column)
                    csvColumns[tm]["columns"].extend(columns)
                    csvColumns[tm]["columns"] = list(dict.fromkeys(csvColumns[tm]["columns"]))
    return csvColumns


def extractReferencesFromFno(functions, columns):
    if 'parameter' in functions:
        functions = functions["value"]
    for parameters in functions["parameters"]:
        if 'parameter' in parameters:
            extractReferencesFromFno(parameters, columns)
        else:
            if re.match("\\$\\(.*\\)", parameters[1]):
                columns.extend(getColumnsfromOM(parameters[1]))
