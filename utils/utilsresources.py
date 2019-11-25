import re
import os
import yaml

def downloadAnnotations(config):
    for key in config:
        source = config[key]
        if re.match("^http.*", source):
            filename = source.split("/")[len(source.split("/")) - 1]
            os.system("wget -O ./tmp/annotations/" + filename + " " + source)
        else:
            os.system("mv " + source + " ./tmp/annotations/")


def downloadCSVfilesFromRML(yarrrml):
    yarrrml = yarrrml.split("/")[len(yarrrml.split("/")) - 1]
    mapping = yaml.load(open("./tmp/annotations/"+yarrrml), Loader=yaml.FullLoader)
    for tm in mapping["mappings"]:
        source = mapping["mappings"][tm]["sources"][0][0]
        if re.match("^http.*", source):
            filename = re.sub("~csv", "", mapping["mappings"][tm]["sources"][0][0].split("/")[
                len(mapping["mappings"][tm]["sources"][0][0].split("/")) - 1])
            os.system("wget -O ./tmp/csv/" + filename + " " + re.sub("~csv", source))
        else:
            os.system("mv " + re.sub("~csv", "", source) + " ./tmp/csv/")


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
