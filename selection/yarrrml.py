import yaml
import re
import json


def getCleanYarrrml ():
    """
    Generate RML mapping without functions:
        - yarrrml mapping

    return dict with the functions (mapping and reference where to apply them) and rml mapping in disk
    """
    functions = {}
    data = yaml.load(open("./tmp/annotations/mapping.yaml"), Loader=yaml.FullLoader)
    for tm in data["mappings"]:
        i = 0
        source = data["mappings"][tm]["sources"][0][0]
        for pom in data["mappings"][tm]["po"]:
            if 'p' in pom:
                predicate = re.sub("^.*:", "", pom["p"])
                object = pom["o"]
                #if it is a basic function
                if 'function' in object[0]:
                    if tm not in functions.keys():
                        functions[tm] = []
                    functions[tm].append({"source": source, "params": object[0], "column": predicate})
                    data["mappings"][tm]["po"][i] = [pom["p"], "$("+predicate+")"]
                #if it is a join
                else:
                    t = 0
                    for jc in object:
                        parameters = jc["condition"]["parameters"]
                        j = 0
                        for param in parameters:
                            if 'parameter' in param:
                                if tm not in functions.keys():
                                    functions[tm] = []
                                if param["parameter"] == 'str1':
                                    functions[tm].append({"source": source, "params": param, "column": predicate})
                                    data["mappings"][tm]["po"][i]["o"][t]["condition"]["parameters"][j] = [
                                        param["parameter"], "$(" + predicate + "_child)"]
                                else:
                                    parent_source = data["mappings"][jc["mapping"]]["source"][0][0]
                                    functions[tm].append({"source": parent_source, "params": param, "column": predicate})
                                    data["mappings"][tm]["po"][i]["o"][t]["condition"]["parameters"][j] = [
                                        param["parameter"], "$(" + predicate + "_parent)"]
                            j += 1
                        t += 1
            i += 1
    return functions, data


# change source by table in the mapping for translating to R2RML
def fromSourceToTables(mapping):

    for tm in mapping["mappings"]:
        source = mapping["mappings"][tm]["sources"][0][0].split("/")[
            len(mapping["mappings"][tm]["sources"][0][0].split("/")) - 1]
        re.sub("\\.csv~csv", "", source)
        mapping["mappings"][tm]["sources"] = [{"table": source.upper()}]
