package es.upm.fi.dia.oeg.rdb;

import es.upm.fi.dia.oeg.model.CSV;
import es.upm.fi.dia.oeg.model.CSVW;
import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class CSVWUtils {



    public static String fromBasetoDatatype(String base){
        String rdbDatatype="VARCHAR(MAX)";
        switch (base){
            case "date":
                rdbDatatype = "DATE";
                break;
            case "integer":
                rdbDatatype = "INT";
                break;
            case "double":
                rdbDatatype = "DOUBLE";
                break;
            case "boolean":
                rdbDatatype = "BOOLEAN";
                break;
            case "float":
                rdbDatatype = "FLOAT";
                break;
            case "datatetime":
                rdbDatatype = "TIMESTAMP";
                break;

        }
        return rdbDatatype;
    }

    public static JSONArray getAnnotationsFromSource (JSONArray tables, CSV csv){
        JSONArray annotations = null;
        for(Object o : tables){
            JSONArray aux = ((JSONObject) o).getJSONObject("tableSchema").getJSONArray("columns");
            String ansource = ((JSONObject)o).getString("url");
            if(ansource.equals(csv.getUrl())){
                annotations = aux;
                break;
            }
            else if(csv.getParentUrl()!=null && ansource.equals(csv.getParentUrl())){
                annotations = aux;
                break;
            }
        }


        return annotations;

    }

    public static JSONObject getCSVWFromSource (JSONArray tables, String csv){
        JSONObject annotations = null;
        for(Object o : tables){
            String ansource = ((JSONObject)o).getString("url");
            if(ansource.equals(csv)){
                annotations = (JSONObject) o;
                break;
            }
        }
        return annotations;

    }

    public static JSONObject annotationForID(){
        JSONObject id = new JSONObject();
        HashMap<String,String> datatype = new HashMap<>();
        datatype.put("base","integer");
        id.put("titles","id");
        id.put("datatype",datatype);


        return id;
    }

    public static JSONObject annotationForJOIN(String column){
        JSONObject id = new JSONObject();
        HashMap<String,String> datatype = new HashMap<>();
        datatype.put("base","integer");
        id.put("titles",column+"_J");
        id.put("datatype",datatype);
        return id;
    }

    public static List<String> getDefaultHeaders(String url, CSVW csvw){
        List<String> defaultHeaders = new ArrayList<>();

        JSONArray tables = (JSONArray) csvw.getContent().get("tables");
        //FN1
        for(Object o : tables){
            String csvURL = ((JSONObject) o).getString("url");
            if(url.equals(csvURL)) {
                JSONArray columns = ((JSONObject) o).getJSONObject("tableSchema").getJSONArray("columns");
                for (Object c : columns) {
                    JSONObject annotations = (JSONObject) c;
                    if (annotations.has("default")) {
                        defaultHeaders.add(annotations.getString("titles"));
                    }
                }
            }
        }

        return defaultHeaders;

    }

    public static String getTile(JSONObject annotation){
        try {
            annotation.getString("titles");
            return annotation.getString("titles");
        }catch (Exception e) {
            JSONArray j = annotation.getJSONArray("titles");
            return j.join("").replaceAll("\"", "");
        }
    }

    public static String getDatatype(JSONObject annotation) {
        try {
            return annotation.getString("datatype");
        }catch (Exception e){
            return annotation.getJSONObject("datatype").getString("base");
        }
    }

    public static String getFormat(JSONObject annotation){
        try{
            return annotation.getJSONObject("datatype").getString("format");
        } catch (Exception e) {
            return null;
        }


    }
}
