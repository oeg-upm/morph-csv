import os
import json
from flask import Flask 
from flask import request


app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")


@app.route('/runmorphcsv', methods=["POST"])
def runmorphcsv():
    csvwLink = request.form['csvwLink']
    yarrrmlLink = request.form['yarrrmlLink']
    queryLink = request.form['queryLink']
    csvwFile = request.files['csvwFile']
    yarrrmlFile = request.files['yarrrmlFile']
    queryFile = request.files['queryFile']    
    yarrrmlError = False
    csvwError = False
    queryError = False
    
    if(csvwLink== '' and csvwFile.filename == ''):
        print("Falta el CSVW")
        csvwError = True
    if(yarrrmlLink== '' and yarrrmlFile.filename == ''):
        print("Falta yarrml mapping")
        yarrrmlError = True
    if(queryLink == '' and queryFile.filename == ''):
        print("Falta la Query")
        queryError = True

    if(not queryError and not csvwError and not yarrrmlError):
        print("Everything Okay")
        csvwPath = csvwLink
        if(csvwFile.filename != ''):
            csvwPath = '/data/annotation.json'
            csvwFile.save(csvwPath)

        yarrrmlPath = yarrrmlLink
        if(yarrrmlFile.filename != ''):
            yarrrmlPath = '/data/annotation.json'
            yarrrmlFile.save(csvwPath)            
        
        if(queryFile.filename != ''):
            queryFile.save('/data/query.rq')
        else:
            os.system("wget -O /data/query.rq " + queryLink)
        morphcsvConfig =  {'csvw':csvwPath,'yarrrml':yarrrmlPath}
        f = open('/data/config.json', 'w')
        f.write(json.dumps(morphcsvConfig))
        f.close()
        os.system("bash /morphcsv/runFromServer.sh")
    else:
        print("Fails....")

    return 'Heloo World'

if __name__ == '__main__':
    app.run()

