from rdflib.plugins import sparql
import xmltodict
import json

def readxml(path):
    data = xmltodict.parse(open(path, encoding='utf-8').read())
    result = {'head':[],'data':[]}
    result['head'] = [{'title':var['@name'],'index':var['@name'], 'key':var['@name']} for var in data['sparql']['head']['variable']]
    for b in data['sparql']['results']['result']:
        aux = {}
        for r in b["binding"]:
            value = 'uri' if 'uri' in r.keys() else 'literal'
            aux[r['@name']] = r[value]
        result['data'].append(aux)
    f = open(path.replace('.xml', '.json'), 'w')
    f.write(json.dumps(result, indent=2))

readxml("/morph-rdb/data/results.xml")

