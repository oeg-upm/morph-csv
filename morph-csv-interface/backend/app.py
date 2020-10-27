import os
import json
from flask import Flask
from flask import request
from flask import jsonify

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object("config.DevelopmentConfig")

tmpFolder = "./tmp/"
@app.route('/runmorphcsv', methods=["POST"])
def runmorphcsv():
    print(request.form)

    csvwLink = request.form['csvwLink'] if ('csvwLink' in request.form.keys()) else ""  
    yarrrmlLink = request.form['yarrrmlLink'] if ('yarrrmlLink' in request.form.keys()) else ""
    queryLink = request.form['queryLink'] if ('queryLink' in request.form.keys()) else ""
    csvwFile = request.files['csvwFile'] if ('csvwFile' in request.files.keys()) else {}
    yarrrmlFile = request.files['yarrrmlFile'] if ('yarrrmlFile' in request.files.keys()) else {}
    queryFile = request.files['queryFile'] if ('queryFile' in request.files.keys()) else {}
    yarrrmlError = False
    csvwError = False
    queryError = False

    if(csvwLink == '' and len(csvwFile.keys()) == 0):
        print("Falta el CSVW")
        csvwError = True
    if(yarrrmlLink== '' and len(yarrrmlFile.keys()) == 0):
        print("Falta yarrml mapping")
        yarrrmlError = True
    if(queryLink == '' and len(queryFile.keys()) == 0):
        print("Falta la Query")
        queryError = True

    if(not queryError and not csvwError and not yarrrmlError):
        print("Everything Okay")
        csvwPath = csvwLink
        if(len(csvwFile.keys()) > 0):
            csvwPath = tmpFolder + 'annotation.json'
            csvwFile.save(csvwPath)

        yarrrmlPath = yarrrmlLink
        if(len(yarrrmlFile.keys()) > 0):
            yarrrmlPath = tmpFolder + 'annotation.json'
            yarrrmlFile.save(csvwPath)

        if(len(queryFile.keys()) > 0):
            queryFile.save(tmpFolder + 'query.rq')
        else:
            os.system("wget -O " + tmpFolder +  "query.rq " + queryLink)
        morphcsvConfig =  {'csvw':csvwPath,'yarrrml':yarrrmlPath}
        f = open(tmpFolder + 'config.json', 'w')
        f.write(json.dumps(morphcsvConfig))
        f.close()
        os.system("bash /morphcsv/runFromServer.sh")
    else:
        print("Fails....")

    return jsonify({'message':'Heloo World'})

if __name__ == '__main__':
    app.run()

