package es.upm.fi.dia.oeg.utils;


import org.apache.commons.io.IOUtils;
import org.json.JSONArray;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Utils {

    private static final Logger _log = LoggerFactory.getLogger(Utils.class);


    public static JSONArray readConfiguration (String config){
        JSONObject jsonObject = new JSONObject();

        try {
            jsonObject = new JSONObject(IOUtils.toString(new FileReader(config)));
        }catch (Exception e){
            _log.error("Exception reading the configuration file: "+e.getMessage());
        }

        return jsonObject.getJSONArray("sources");
    }

    public static boolean checkRDBInstance(String dbName){
        final boolean[] flag = {false};
        String path ="./output/"+dbName+".mv.db";
        try (Stream<Path> walk = Files.walk(Paths.get("./output"))) {

            List<String> results = walk.filter(Files::isRegularFile)
                    .map(x -> x.toString()).collect(Collectors.toList());

            results.forEach(result -> {
                if(result.equals(path)){
                    flag[0]=true;
                }
            });
        } catch (IOException e) {
            _log.error("Error checking the RDB instances: "+e.getMessage());
        }
        return flag[0];
    }



}
