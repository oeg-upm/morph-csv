package es.upm.fi.dia.oeg.rdb;

import es.upm.fi.dia.oeg.model.CSV;
import es.upm.fi.dia.oeg.model.CSVW;
import es.upm.fi.dia.oeg.rmlc.api.model.*;
import org.json.JSONArray;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;

public class RDBUtils {
    private String schema;
    private static final Logger _log = LoggerFactory.getLogger(RDBUtils.class);

    public String  createSQLSchema(Collection<TriplesMap> triplesMaps, ArrayList<CSV> csvs, CSVW csvw){
        schema = "";

        triplesMaps.forEach(triplesMap -> {
            for(CSV csv : csvs){
                if(csv.getUrl().equals(((Source)triplesMap.getLogicalSource()).getSourceName())){
                    schema += createTable(triplesMap,csv,csvs,csvw);
                    break;
                }
            }
        });
        return schema;
    }

    public String createTable(TriplesMap tripleMap, CSV csv, ArrayList<CSV> csvs, CSVW csvw){
        MappingUtils m = new MappingUtils();
        String[] headers =null;
        if(csv.getRows()==null) {
              for(CSV c: csvs){
                  if(c.getUrl().equals(csv.getParentUrl())){
                      headers = c.getRows().get(0);
                  }
              }
        }
        else
            headers = csv.getRows().get(0);

        ArrayList<String> primaryKeys = m.getPrimaryKeys(tripleMap,csvw,csv.getParentUrl());
        String sourceUrl = ((Source)tripleMap.getLogicalSource()).getSourceName();
        HashMap<String,ArrayList<String>> foreignKeys = m.getForeignKeys(tripleMap);
        JSONArray annotations = CSVWUtils.getAnnotationsFromSource(csvw.getContent().getJSONArray("tables"),csv);
        String tableName = sourceUrl.split("/")[sourceUrl.split("/").length-1].replace(".csv","").toUpperCase();
        String table="DROP TABLE IF EXISTS "+tableName+";\nCREATE TABLE "+tableName+" ";
        table+="(";
        for(String field : headers){
            if(checkColumnInAnnotations(field,tripleMap,csvw)) {
                String datatype = null;
                Object def=null;
                for (Object o : annotations) {
                    String column = CSVWUtils.getTile((JSONObject) o);
                    if (column.equals(field.trim())) {
                        if (((JSONObject) o).has("datatype")) {
                            datatype = CSVWUtils.getDatatype((JSONObject) o);
                        }
                        if(((JSONObject) o).has("default")){
                            def = ((JSONObject) o).get("default");

                        }
                    }

                }
                if(datatype!=null) {
                    table += "`" + field.toLowerCase().trim() + "` " + CSVWUtils.fromBasetoDatatype(datatype);
                }
                else
                    table += "`" + field.toLowerCase().trim() + "` VARCHAR(MAX)";
                if(def!=null)
                    table += " DEFAULT '"+def.toString()+"'";
                /*if(required!=null)
                    table += " NOT NULL";*/
                table += ",";
            }
        }

        table=table.substring(0,table.length()-1);
        if(!primaryKeys.isEmpty()) {
            table += ",PRIMARY KEY (";
            for (String p : primaryKeys) {
                table += p + ",";
            }
            table=table.substring(0,table.length()-1);
            table += ")";
        }

        if(!foreignKeys.isEmpty()) {
            for(Map.Entry<String, ArrayList<String>> entry : foreignKeys.entrySet()){
                table += ",FOREIGN KEY ("+entry.getValue().get(0)+") REFERENCES "+entry.getKey()+" ("+entry.getValue().get(1)+")";

            }
        }


        table+=");\n";
        //System.out.println(table);
        return table;
    }


    public static boolean checkColumnInAnnotations(String header, TriplesMap triplesMap, CSVW csvw){
        boolean flag = false;
        MappingUtils m = new MappingUtils();
        if(triplesMap.getSubjectMap().getTemplate().getColumnNames().contains(header.trim())){
            flag= true;
        }
        else if(m.getPrimaryKeys(triplesMap,csvw,"").contains(header)){
            flag=true;
        }
        else {
            for(PredicateObjectMap pom : triplesMap.getPredicateObjectMaps()){
                for(ObjectMap ob : pom.getObjectMaps()){
                    if(ob.getColumn()!=null){
                        if(ob.getColumn().matches(".*"+header.trim()+".*")){
                            flag = true;
                        }
                    }
                    else if(ob.getTemplate()!=null){
                        if(ob.getTemplate().getColumnNames().contains(header.trim())){
                            flag = true;
                        }
                    }
                }
                for(RefObjectMap refObjectMap : pom.getRefObjectMaps()){
                    if(refObjectMap.getJoinCondition(0).getChild().matches(".*"+header.trim()+".*")){
                        flag= true;
                    }
                }
            }
        }

        return flag;
    }


    public HashMap<String,String> getColumnsFromFunctions(List<PredicateObjectMap> predicateObjectMaps){
        HashMap<String,String> columnsFunctions = new HashMap<>();

        for(PredicateObjectMap p : predicateObjectMaps){
            List<ObjectMap> objectMaps = p.getObjectMaps();
            for(ObjectMap o : objectMaps){
                if(o.getFunction()!=null && !o.getFunction().isEmpty()){
                    List<PredicateMap> predicateMaps = p.getPredicateMaps();
                    for(PredicateMap pm : predicateMaps){
                        String t= pm.getConstant().ntriplesString();
                        if(t.matches(".*#.*"))
                            columnsFunctions.put(t.split("#")[1].replace(">","") + " VARCHAR(MAX)",o.getFunction());
                        else
                            columnsFunctions.put(t.split("/")[t.split("/").length-1].replace(">","")+ " VARCHAR(MAX)",o.getFunction());
                    }
                }
            }
        }
        return columnsFunctions;

    }

    public HashMap<String,HashMap<String,String>> getJoinFunctions(List<PredicateObjectMap> predicateObjectMaps, String child_table_name){
        HashMap<String,HashMap<String,String>> joinFunction = new HashMap<>();
        for(PredicateObjectMap p : predicateObjectMaps){
            List<RefObjectMap> refObjectMaps = p.getRefObjectMaps();
            List<PredicateMap>  predicateMaps = p.getPredicateMaps();
            for(RefObjectMap refObjectMap : refObjectMaps){
                String parent_table_name = ((Source) refObjectMap.getParentMap().getLogicalSource()).getSourceName();
                parent_table_name = parent_table_name.split("/")[parent_table_name.split("/").length-1].replace(".csv","").toUpperCase();
                List<Join> join = refObjectMap.getJoinConditions();
                for(Join j : join ){
                    String child_function = j.getChild();
                    String parent_function = j.getParent();
                    for(PredicateMap pm : predicateMaps){
                        HashMap<String, String> functions_column = new HashMap<>();
                        String t;
                        if(pm.getConstant().ntriplesString().matches(".*#.*"))
                            t= pm.getConstant().ntriplesString().split("#")[1].replace(">","");
                        else
                            t = pm.getConstant().ntriplesString().split("/")[pm.getConstant().ntriplesString().split("/").length-1].replace(">","");
                        boolean indexs=false;
                        if(!parent_function.isEmpty() && parent_function.matches(".*\\(.*")) {
                            functions_column.put(t+"_parent VARCHAR(MAX)", parent_function);
                            if(joinFunction.containsKey(parent_table_name)){
                                joinFunction.get(parent_table_name).putAll((HashMap<String, String>) functions_column.clone());
                            }
                            else {
                                joinFunction.put(parent_table_name, (HashMap<String, String>) functions_column.clone());
                            }
                            indexs = true;
                        }
                        functions_column.clear();
                        if((!child_function.isEmpty() && child_function.matches(".*\\(.*")) || indexs) {
                            if((!child_function.isEmpty() && child_function.matches(".*\\(.*"))) {
                                functions_column.put(t+"_child VARCHAR(MAX)", child_function);
                                if(joinFunction.containsKey(child_table_name)) {
                                    joinFunction.get(child_table_name).putAll((HashMap<String, String>) functions_column.clone());
                                }
                                else
                                    joinFunction.put(child_table_name, (HashMap<String, String>) functions_column.clone());
                            }
                            else{
                                String child = child_function.replace("{","").replace("}","");
                                functions_column.put(child+"_child VARCHAR(MAX)",child_function);
                                if(joinFunction.containsKey(child_table_name)){
                                    joinFunction.get(child_table_name).putAll((HashMap<String, String>) functions_column.clone());
                                }
                                else
                                    joinFunction.put(child_table_name, (HashMap<String, String>) functions_column.clone());
                            }
                        }
                        functions_column.clear();

                    }
                }
            }
        }
        return joinFunction;

    }



}
