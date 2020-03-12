package es.upm.fi.dia.oeg.utils;

import es.upm.fi.dia.oeg.model.RDB;
import es.upm.fi.dia.oeg.morph.base.engine.MorphBaseRunner;
import es.upm.fi.dia.oeg.morph.r2rml.rdb.engine.MorphRDBRunnerFactory;
import org.json.JSONArray;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;

public class RunQuery {


    static Logger log = LoggerFactory.getLogger(RunQuery.class);
    //run morph
    public static void runBatchMorph(RDB rdb){
        String configurationFile = "output/"+rdb.getName()+".r2rml.properties";
        setProperties(rdb,null,null);

        try {
            MorphRDBRunnerFactory runnerFactory = new MorphRDBRunnerFactory();
            MorphBaseRunner runner = runnerFactory.createRunner(".",configurationFile);
            runner.run();
            log.info("Materialization made correctly");
        } catch(Exception e) {
            e.printStackTrace();
            log.info("Error occured: " + e.getMessage());
        }

    }

    public static void runQueryMorph(RDB rdb, JSONArray queries){
        for(Object query: queries) {
            String queryName = (String) query;
            queryName=queryName.split("/")[queryName.split("/").length-1].replace(".rq","");
            String configurationFile = "output/"+rdb.getName()+"-"+queryName+".r2rml.properties";
            setProperties(rdb, (String)query, queryName);
            try {
                MorphRDBRunnerFactory runnerFactory = new MorphRDBRunnerFactory();
                MorphBaseRunner runner = runnerFactory.createRunner(".", configurationFile);
                runner.run();
                log.info("Evaluation query correctly");
            } catch (Exception e) {
                e.printStackTrace();
                log.info("Error occured: " + e.getMessage());
            }
        }
    }

    private static void setProperties(RDB rdb, String query, String queryName){
        try {
            PrintWriter writer;

            if(query!=null) {
                writer = new PrintWriter("output/"+rdb.getName()+"-"+queryName+".r2rml.properties", "UTF-8");
                writer.println("query.file.path=" + query);
                writer.println("output.file.path=output/" + rdb.getName() + "-"+queryName+"-result.xml");
            }
            else {
                writer = new PrintWriter("output/"+rdb.getName() + ".r2rml.properties", "UTF-8");
                writer.println("output.file.path=output/" + rdb.getName() + "-batch-result.xml");
            }
            writer.println("mappingdocument.file.path=output/"+ rdb.getName() + ".r2rml.ttl");
            writer.println("database.name[0]=" + rdb.getName());
            writer.println("no_of_database=1");
            writer.println("database.driver[0]=org.h2.Driver");
            writer.println("database.url[0]=jdbc:h2:./output/" + rdb.getName());
            writer.println("database.user[0]=sa");
            writer.println("database.pwd[0]=");
            writer.println("database.type[0]=h2");

            writer.close();
        }catch (Exception e ){
            log.info("Error writing the resources for morph-rdb...");
        }
    }

    //run ontop


}
