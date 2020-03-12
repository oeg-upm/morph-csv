package es.upm.fi.dia.oeg.rdb;

import es.upm.fi.dia.oeg.model.*;

import es.upm.fi.dia.oeg.rmlc.api.model.*;
import org.json.JSONArray;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class RDBGenerator {

    private static final Logger _log = LoggerFactory.getLogger(RDBGenerator.class);
    private RMLCMapping rmlc;
    private CSVW csvw;
    private ArrayList<CSV> csvs;
    private RDB rdb;


    public RDBGenerator(Dataset d){
       rmlc = d.getRmlcMappingY();
       csvw = d.getCsvw();
       csvs = d.getCsvFiles();
    }

    public RDB generateSchemaRDB(String name){

        normalize();
        String schema=createTables();
        rdb = new RDB(name,schema);
        return rdb;
    }

    private void normalize(){

        JSONArray tables = (JSONArray) csvw.getContent().get("tables");
        //FN1
        _log.info("Normalizing to FN1 the CSV files");
        for(Object o : tables){
            String csvURL = ((JSONObject) o).getString("url");
            boolean header=false;
            if((((JSONObject) o).getJSONObject("tableSchema")).has("rowTitles")){
                if(((JSONObject) o).has("dialect")){
                    JSONObject dialect = ((JSONObject) o).getJSONObject("dialect");
                    if(dialect.has("header")){
                        header=dialect.getBoolean("header");
                    }
                }
                JSONArray rows = (((JSONObject) o).getJSONObject("tableSchema")).getJSONArray("rowTitles");
                String[] csvHeader = rows.join(",").replaceAll("\"", "").split(",");
                for (CSV csv : csvs) {
                    if (csvURL.equals(csv.getUrl())) {
                        if(!header)
                            csv.getRows().add(0, csvHeader);
                        else
                            csv.getRows().set(0,csvHeader);
                    }
                }

            }
            JSONArray columns = ((JSONObject) o).getJSONObject("tableSchema").getJSONArray("columns");
            JSONArray newAnnotations = new JSONArray();
            List<String[]> newCSV = new ArrayList<>();
            for(Object c : columns){
                if(((JSONObject) c).has("null")){
                    for(CSV csv: csvs) {
                        if(csv.getUrl().equals(csvURL)){
                            CSVUtils.putNull(csv.getRows(),(JSONObject) c);
                        }
                        else if(csv.getParentUrl()!=null && csv.getParentUrl().equals(csvURL)){
                            CSVUtils.putNull(csv.getRows(),(JSONObject) c);
                        }
                    }
                }
                if(((JSONObject) c).has("separator")){
                    //create a new csv
                    String separator = ((JSONObject) c).getString("separator");
                    String column = CSVWUtils.getTile((JSONObject) c);
                    for(CSV csv: csvs){
                        if(csv.getUrl().equals(csvURL)){
                            MappingUtils u = new MappingUtils();
                            //create new csv
                            newCSV = CSVUtils.generateCSVfromSeparator(separator,column,csv.getRows());
                            //remove the column
                            csv.setRows(CSVUtils.removeSeparetedColumn(column,csv.getRows()));
                            //edit rmlcmappingnada nad
                            String newRMLC = u.generateTriplesMapfromSeparator(newCSV.get(0),rmlc,csvURL);
                            JSONObject idannotations = CSVWUtils.annotationForID();
                            newAnnotations.put(idannotations);
                            idannotations = CSVWUtils.annotationForJOIN(column);
                            newAnnotations.put(idannotations);
                            rmlc.setContent(newRMLC);
                            rmlc.setTriples(rmlc.getContent());

                        }
                    }
                    csvs.add(new CSV(column,column+".csv",csvURL,newCSV));
                }

                if(((JSONObject) c).has("datatype")){
                    String datatype = CSVWUtils.getDatatype((JSONObject) c);
                    String format = CSVWUtils.getFormat((JSONObject) c);
                    String column = CSVWUtils.getTile((JSONObject) c);
                    if(format!=null && datatype.equals("date")){
                        for(CSV csv : csvs){
                            if(csv.getUrl().equals(csvURL)){
                                CSVUtils.changeFormat(column,csv.getRows(),(JSONObject)c);
                            }
                            else if(csv.getParentUrl()!=null && csv.getParentUrl().equals(csvURL)){
                                CSVUtils.changeFormat(column,csv.getRows(),(JSONObject)c);
                            }
                        }
                    }
                }
                if(((JSONObject)c).has("default")){
                    for(CSV csv: csvs){
                        if(csv.getUrl().equals(csvURL)){
                            CSVUtils.putDefault(csv.getRows(),(JSONObject) c);
                        }
                        else if(csv.getParentUrl()!=null && csv.getParentUrl().equals(csvURL)){
                            CSVUtils.putDefault(csv.getRows(),(JSONObject) c);
                        }
                    }
                }
            }
            for(Object c: newAnnotations){
                columns.put(c);
            }
        }

        //FN2
        _log.info("Normalizing to FN2 the CSV files");
        HashMap<String, Boolean> sources = new HashMap<>();
        rmlc.getTriples().forEach(triplesMap -> {
            if(sources.get(((Source)triplesMap.getLogicalSource()).getSourceName())==null)
               sources.put(((Source)triplesMap.getLogicalSource()).getSourceName(),false);
            else
               sources.put(((Source)triplesMap.getLogicalSource()).getSourceName(),true);
        });

        for(Map.Entry<String, Boolean> entry : sources.entrySet()){
            if(entry.getValue()){
                ArrayList<TriplesMap> triplesMaps = new ArrayList<>();
                rmlc.getTriples().forEach(tp -> {
                    if(((Source)tp.getLogicalSource()).getSourceName().equals(entry.getKey())){
                        triplesMaps.add(tp);
                    }
                });

                for(TriplesMap t : triplesMaps){
                    String newSourceName=""; TriplesMap aux=null;
                    for(PredicateObjectMap pom : t.getPredicateObjectMaps()){
                        for(RefObjectMap ob : pom.getRefObjectMaps()){
                            String columnWithoutColumns = ob.getParentMap().getSubjectMap().getTemplate().getTemplateStringWithoutColumnNames().
                                    replace("{","").replace("}-","").replace("}","");
                            String pkExpresion= ob.getParentMap().getSubjectMap().getTemplateString().replace(columnWithoutColumns,"");
                            ob.getJoinCondition(0).setChild(pkExpresion);
                            ob.getJoinCondition(0).setParent(pkExpresion);
                            newSourceName = ob.getParentMap().getNode().ntriplesString().replace(">","").replace("<","");
                            aux = ob.getParentMap();

                        }
                    }
                    if(newSourceName!="" && aux!=null){
                        String oldSource = ((Source)aux.getLogicalSource()).getSourceName();
                        ((Source)aux.getLogicalSource()).setSourceName(newSourceName+".csv");
                        csvs.add(new CSV(newSourceName,newSourceName+".csv",oldSource,null));
                    }
                }
            }
        }


    }

    private String createTables(){
        _log.info("Generating the schema of the RDB");
        RDBUtils rdbUtils = new RDBUtils();
        return rdbUtils.createSQLSchema(rmlc.getTriples(),csvs,csvw);
    }

    public void generateRDB(){

        _log.info("Creating the RDB");
        long startTime = System.currentTimeMillis();
        RDBConexion rdbConexion = new RDBConexion(rdb.getName());
        rdbConexion.createDatabase(rdb.getName(),rdb.getContent());
        HashMap<String,HashMap<String,String>> functions = new HashMap<>();
        HashMap<String,HashMap<String,String>> joinFunctions = new HashMap<>();

        rmlc.getTriples().forEach(triplesMap -> {
            for(CSV csv : csvs){
                if(csv.getUrl().equals(((Source)triplesMap.getLogicalSource()).getSourceName())){
                    String sourceUrl = ((Source) triplesMap.getLogicalSource()).getSourceName();
                    String tableName = sourceUrl.split("/")[sourceUrl.split("/").length-1].replace(".csv","").toUpperCase();
                    if(csv.getRows()==null){
                        String url = csv.getParentUrl();
                        for(CSV aux: csvs){
                            if(aux.getUrl().equals(url)){
                                rdbConexion.loadCSVinTable(triplesMap,aux.getRows(),tableName,rdb.getName(),csvw);
                                break;
                            }
                        }

                    }
                    else {
                       rdbConexion.loadCSVinTable(triplesMap, csv.getRows(), tableName, rdb.getName(),csvw);
                    }
                    break;
                }
            }
        });
        rdbConexion.addForeignKeys(rdb.getName());
        rmlc.getTriples().forEach(triplesMap -> {
            RDBUtils rdbutils = new RDBUtils();
            String sourceUrl = ((Source)triplesMap.getLogicalSource()).getSourceName();
            String tableName =sourceUrl.split("/")[sourceUrl.split("/").length-1].replace(".csv","").toUpperCase();
            functions.put(tableName,rdbutils.getColumnsFromFunctions(triplesMap.getPredicateObjectMaps()));
            joinFunctions.putAll(rdbutils.getJoinFunctions(triplesMap.getPredicateObjectMaps(),tableName));
        });
        rdbConexion.updateDataWithFunctions(functions,rdb.getName(),false);
        rdbConexion.updateDataWithFunctions(joinFunctions,rdb.getName(),true);
        rdbConexion.close();
        long stopTime = System.currentTimeMillis();
        long elapsedTime = stopTime - startTime;
        _log.info("Total time of creation: "+elapsedTime+"ms");
    }



}
