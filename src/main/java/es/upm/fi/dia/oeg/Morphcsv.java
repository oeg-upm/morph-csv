package es.upm.fi.dia.oeg;

import es.upm.fi.dia.oeg.model.Dataset;
import es.upm.fi.dia.oeg.model.RDB;
import es.upm.fi.dia.oeg.rdb.RDBGenerator;
import es.upm.fi.dia.oeg.translation.RMLC2R2RML;
import es.upm.fi.dia.oeg.translation.yarrrml2RMLC;
import es.upm.fi.dia.oeg.utils.CommandLineProcessor;
import es.upm.fi.dia.oeg.utils.RunQuery;
import es.upm.fi.dia.oeg.utils.Utils;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.Option;
import org.json.JSONArray;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.xml.crypto.Data;
import java.util.ArrayList;


/**
 * Morph-CSV: RDF Mapping Language for heterogeneous CSV files
 * @author : David Chaves
 */
public class Morphcsv
{
    private static final Logger _log = LoggerFactory.getLogger(Morphcsv.class);

    public static void main( String[] args )
    {

        org.apache.log4j.BasicConfigurator.configure();
        CommandLine commandLine = CommandLineProcessor.parseArguments(args);

        if(commandLine.getOptions().length < 1 || commandLine.getOptions().length > 2 ){
            CommandLineProcessor.displayHelp();
        }



       String configPath = commandLine.getOptionValue("c");
       JSONArray config = Utils.readConfiguration(configPath);
       for(Object aux : config){
           JSONObject c = (JSONObject) aux;
           Dataset dataset = new Dataset(c.getString("db"));
           if(!Utils.checkRDBInstance(c.getString("db"))) {
               dataset = new Dataset(c.get("csvw").toString(), c.get("yarrrml").toString());
               _log.info("Translating YARRRML mapping to RMLC...");

               //set rmlc mapping from yarrrml after the translation and csv web
               //dataset.setRmlcMappingC(CSVW2RMLC.translateCSVW2RMLC(dataset.getCsvw()));
               dataset.setRmlcMappingY(yarrrml2RMLC.translateYarrrml2RMLC(dataset.getYarrrmlMapping()));

               //generate RDB
               _log.info("Generating the schema of the RDB");
               RDBGenerator rdbGenerator = new RDBGenerator(dataset);
               dataset.setRdb(rdbGenerator.generateSchemaRDB(c.get("db").toString()));
               //load RDB
               rdbGenerator.generateRDB();
               //generate R2RML
               _log.info("Translating RMLC to R2RML...");
               RMLC2R2RML rmlc2R2RML = new RMLC2R2RML();
               rmlc2R2RML.generateR2RML(dataset.getRmlcMappingY(), dataset.getRdb().getName());
               dataset.setR2rmlMapping(rmlc2R2RML.getR2RML());
           }
           else{
               _log.info("The RDB "+dataset.getRdb().getName()+" has already generated");
           }
           //execute query

           if(c.has("query")){
               _log.info("Executing query with morph-rdb");
               RunQuery.runQueryMorph(dataset.getRdb(),c.getJSONArray("query"));
           }
           else{
               _log.info("Executing materialization with morph-rdb");
              RunQuery.runBatchMorph(dataset.getRdb());
           }
        }
    }
}
