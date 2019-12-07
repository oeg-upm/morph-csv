import re
import sys
import os
import yaml

def downloadAnnotations(config):
    for key in config:
        source = config[key]
        extension = source.split(".")[len(source.split(".")) - 1]
        if re.match("json", extension):
            name = "annotations.json"
        elif re.match("yml || yaml", extension):
            name = "mapping.yaml"
        if re.match("^http.*", source):
            os.system("wget -O ./tmp/annotations/" + name + " " + source)
        else:
            os.system("cp " + source + " ./tmp/annotations/" + name)


def downloadCSVfilesFromRML():
    mapping = yaml.load(open("./tmp/annotations/mapping.yaml"), Loader=yaml.FullLoader)
    for tm in mapping["mappings"]:
        source = mapping["mappings"][tm]["sources"][0][0]
        if re.match("^http.*", source):
            filename = re.sub("~csv", "", mapping["mappings"][tm]["sources"][0][0].split("/")[
                len(mapping["mappings"][tm]["sources"][0][0].split("/")) - 1])
            os.system("wget -O ./tmp/csv/" + filename + " " + re.sub("~csv","",source))
        else:
            #change to move mv
            # cp is only for test
            os.system("cp ." + re.sub("~csv", "", source) + " ./tmp/csv/")


def readQuery(path):
    with open(path, "r") as file:
        content = file.read()
    return content


def maketmpdirs():
    os.system("mkdir ./tmp/")
    os.system("mkdir ./tmp/annotations")
    os.system("mkdir ./tmp/csv")
    os.system("mkdir ./tmp/morph-properties")
    os.system("mkdir ./results")


def removetmpdirs():
    os.system("rm -r ./tmp")

def sparqlQueryParser(path):
    try:
        os.system("bash bash/sparqlQueryParser.sh %s"%(str(path)))
        print('Query Parsed')
    except:
        print('The Formatt of the query is wrong')
        sys.exit()

