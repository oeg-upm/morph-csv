package es.upm.fi.dia.oeg.iterator;

/*
import es.upm.fi.dia.oeg.Utils;
import es.upm.fi.dia.oeg.rmlc.processor.RMLCIteratorGenerator;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.FileNotFoundException;
import java.io.PrintWriter;

public class IteratorTransformer {

    private Utils utils;


    public IteratorTransformer(Utils utils){
        this.utils = utils;
    }

    public void run(){
        checkAndTransform();
    }

    public void checkAndTransform(){
       JSONArray datasets = utils.getConfig().getJSONArray("datasets");
        for(Object d : datasets){
            String databaseName = (String)((JSONObject) d).get("databaseName");
            String mappingPath = utils.getMappingPath(databaseName);
            String mappingContent = utils.getMappingContent(mappingPath);
            String csvPath = "datasets/"+databaseName;
            if(mappingContent.matches(".*\\{\\$column}.*") || mappingContent.matches(".*\\{\\$alias}.*")){
                convertToGeneralRMLC(mappingPath,csvPath);
            }
        }


    }

    private void convertToGeneralRMLC(String mappingPath, String csvPath){
        RMLCIteratorGenerator rmlcIteratorGenerator = new RMLCIteratorGenerator(mappingPath,csvPath);
        String newmapping=rmlcIteratorGenerator.run();
        try {
            PrintWriter pw = new PrintWriter(mappingPath);
            pw.write(newmapping);
            pw.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

    }
}
*/