package es.upm.fi.dia.oeg.utils;


import org.apache.commons.io.FileUtils;
import org.json.JSONArray;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.net.URL;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class DatasetUnzip {


    private static final Logger _log = LoggerFactory.getLogger(DatasetUnzip.class);

    public static void downloadAndUnzip(JSONArray datasets){
        try {
            for (Object object : datasets) {
                JSONObject dataset = (JSONObject) object;
                String relativePath= "datasets/"+dataset.getString("databaseName");
                File f = new File(relativePath);
                f.mkdir();
                Object source = dataset.get("source");
                if(source instanceof String) {
                    String source_string = (String) source;
                    if (source_string.matches("http.*")) {
                        f = new File(relativePath + "/dataset." + dataset.getString("compression"));
                        FileUtils.copyURLToFile(new URL(source_string), f);
                    }
                    else {
                        f = new File(relativePath + "/data");
                        FileUtils.copyDirectory(new File(source_string), f);
                    }

                    if(dataset.getString("compression").equals("zip")){
                        unzip(relativePath,f.getName());
                        f.delete();
                    }
                    else if(!dataset.getString("compression").isEmpty()){
                        _log.error("The compression of "+dataset.getString("databaseName")+" CSV set should be ZIP");
                    }
                }
                else if (source instanceof JSONArray){
                    JSONArray source_array = (JSONArray) source;
                    for (Object s : source_array){
                        String path = (String) s;
                        String file_name = path.split("\\.csv")[0].split("/")[path.split("\\.csv")[0].split("/").length-1];
                        if(path.matches("http.*")){
                            FileUtils.copyURLToFile(new URL(path),new File(relativePath+"/"+file_name+".csv"));
                        }
                        else{
                            FileUtils.copyFile(new File(path),new File(relativePath+"/"+file_name+".csv"));
                        }
                    }
                }
            }

        }catch (Exception e){
            _log.error("URL is not correct: "+e.getMessage());
        }
    }


    private static void unzip (String path, String name){
        try {
            byte[] buffer = new byte[1024];
            File f = new File(path+"/data");
            f.mkdir();
            ZipInputStream zis = new ZipInputStream(new FileInputStream(path+"/"+name));
            ZipEntry zipEntry = zis.getNextEntry();
            while (zipEntry != null) {
                String fileName = zipEntry.getName();
                File newFile = new File(path+"/data/"+fileName.substring(0,fileName.lastIndexOf("."))+".csv");
                FileOutputStream fos = new FileOutputStream(newFile);
                int len;
                while ((len = zis.read(buffer)) > 0) {
                    fos.write(buffer, 0, len);
                }
                fos.close();
                zipEntry = zis.getNextEntry();
            }
            zis.closeEntry();
            zis.close();
        }catch (Exception e){
            _log.error("Error during unzip process: "+e.getMessage());
        }
    }
}
