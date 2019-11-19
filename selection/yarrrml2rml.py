import yaml
from subprocess import call
import re


def yarrrml2rml (yarrrml):
    """
    Generate RML mapping without functions:
        - yarrrml mapping

    return dict with the functions (mapping and reference where to apply them) and rml mapping in disk
    """
    functions = {}
    data = yaml.load(open(yarrrml), Loader=yaml.FullLoader)
    for tm in data["mappings"]:
        i = 0
        for pom in data["mappings"][tm]["po"]:
            if 'p' in pom:
                if tm not in functions.keys():
                    functions[tm] = []
                predicate = re.sub("^.*:", "", pom["p"])
                object = pom["o"]
                #if it is a basic function
                if 'function' in object[0]:
                    functions[tm].append([predicate, object])
                    data["mappings"][tm]["po"][i] = [pom["p"], "$("+predicate+")"]
                #if it is a join
                else:
                    t = 0
                    for jc in object:
                        parameters = jc["condition"]["parameters"]
                        j = 0
                        for param in parameters:
                            if 'parameter' in param:
                                if param["parameter"] == 'str1':
                                    functions[tm].append([predicate+"_child", param])
                                    data["mappings"][tm]["po"][i]["o"][t]["condition"]["parameters"][j] = [
                                        param["parameter"], "$(" + predicate + "_child)"]
                                else:
                                    functions[tm].append([predicate+"_parent", param])
                                    data["mappings"][tm]["po"][i]["o"][t]["condition"]["parameters"][j] = [
                                        param["parameter"], "$(" + predicate + "_parent)"]
                            j += 1
                        t += 1
            i += 1
    return functions, data


