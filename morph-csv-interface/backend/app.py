import io
import os
import json
from flask import Flask
from flask import request
from flask import jsonify
from flask import send_file
from flask_cors import CORS
from flask_restful import Resource,Api,reqparse
import zipfile
import xmltodict
import json
app = Flask(__name__,static_folder='/server/public', static_url_path='/')
api = Api(app)
CORS(app)

app.config.from_object("config.DevelopmentConfig")

zipResult='/results/results.zip'
tmpFolder = "/server/tmp/"
API_URL = "/runmorphcsv"
morphRdbResultPath="/morph-rdb/data/results.xml"

def readxml(path):
    data = xmltodict.parse(open(path, encoding='utf-8').read())
    result = {'head':[],'data':[]}
    result['head'] = [{'title':var['@name'],'dataIndex':var['@name'], 'key':var['@name']} for var in data['sparql']['head']['variable']]
    for i,b in enumerate(data['sparql']['results']['result']):
        aux = {}
        for r in b["binding"]:
            value = 'uri' if 'uri' in r.keys() else 'literal'
            aux[r['@name']] = r[value]
        aux['key'] = i
        result['data'].append(aux)
    return result



def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def getZipFile():
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        zipdir('/results/annotations/',z)
        zipdir('/results/csv/',z)
    data.seek(0)    
    return data


class Runmorphcsv(Resource):
    def post(self):
        print(request.form)

        csvwLink = request.form['csvwLink'] if ('csvwLink' in request.form.keys()) else ""  
        yarrrmlLink = request.form['yarrrmlLink'] if ('yarrrmlLink' in request.form.keys()) else ""
        queryLink = request.form['queryLink'] if ('queryLink' in request.form.keys()) else ""
        csvwFile = request.files['csvwFile'] if ('csvwFile' in request.files.keys()) else None
        yarrrmlFile = request.files['yarrrmlFile'] if ('yarrrmlFile' in request.files.keys()) else None
        queryFile = request.files['queryFile'] if ('queryFile' in request.files.keys()) else None
        runMorphRdb = 'runMorphRdb' in request.form.keys() 
        yarrrmlError = False
        csvwError = False
        addQuery = False
        qPath = " -f "
        print("*"*10)
        print("RunMorphRdb: " + str(runMorphRdb))
        print("*"*10)
        if(csvwLink == '' and csvwFile == None):
            print("Falta el CSVW")
            csvwError = True
        if(yarrrmlLink== '' and yarrrmlFile == None):
            print("Falta yarrml mapping")
            yarrrmlError = True
        if(queryLink != '' or queryFile != None):
            addQuery = True

        if(not csvwError and not yarrrmlError):
            print("Everything Okay")
            csvwPath = csvwLink
            if(csvwFile != None):
                csvwPath = tmpFolder + 'annotation.json'
                csvwFile.save(csvwPath)

            yarrrmlPath = yarrrmlLink
            if(yarrrmlFile != None):
                yarrrmlPath = tmpFolder + 'mapping.yaml'
                yarrrmlFile.save(yarrrmlPath)
            if(addQuery):
                qPath = '-q ' + tmpFolder + 'query.rq'
                if(queryFile != None):
                    queryFile.save(tmpFolder + 'query.rq')
                else:
                    os.system("wget -O " + tmpFolder +  "query.rq " + queryLink)
            morphcsvConfig =  {'csvw':csvwPath,'yarrrml':yarrrmlPath}
            f = open(tmpFolder + 'config.json', 'w')
            f.write(json.dumps(morphcsvConfig))
            f.close()
            try:
                os.system("bash /morphcsv/bash/runFromServer.sh '%s'"%qPath)
                if(runMorphRdb):
                    os.system("bash /morph-rdb/runMorphRdb.sh %s"%qPath)
                    data = readxml(morphRdbResultPath)
                    return(jsonify(data))
                else:
                   data = getZipFile()
                   return send_file(
                        data,
                        mimetype='application/zip',
                        as_attachment=True,
                        attachment_filename='data.zip'
                        )                    

            except:
                return jsonify({'message':'Something goes wrong...'})
        else:
            return jsonify({'message':'Something goes wrong...'})
api.add_resource(Runmorphcsv,API_URL)          

@app.route('/')
def index():
    return app.send_static_file('index.html')
    
def run(host="0.0.0.0", port=5000):
    print("API_URL: " + API_URL)
    app.run(debug=False,host=host,port=port)

if __name__ == '__main__':
    run()

