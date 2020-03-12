package es.upm.fi.dia.oeg.model;

import org.apache.commons.io.Charsets;
import org.apache.commons.io.IOUtils;
import org.apache.jena.atlas.io.IO;
import org.json.JSONArray;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.stream.Collectors;

public class CSVW {
    private static final Logger _log = LoggerFactory.getLogger(CSVW.class);
    private String url;
    private JSONObject content;

    public CSVW(String url, String content) {
        this.url = url;
        this.content = new JSONObject(content);
    }

    public CSVW(Path path) {
        this.url = path.toString();
        setContent(path);
    }

    public CSVW(URL url) {
        this.url = url.toString();
        setContent(url);
    }

    public JSONObject getContent() {
        return content;
    }

    public void setContent(JSONObject content) {
        this.content = content;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public void setContent (Path path){
        try {
            this.content = new JSONObject(String.join("\n",Files.readAllLines(path, Charsets.toCharset("UTF-8"))));
        }catch (Exception e){
            _log.error("Error reading the CSVW content: "+e.getMessage());
        }
    }

    public void setContent (URL url){
        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(url.openStream()));
            this.content= new JSONObject(IOUtils.toString(reader));

        }catch (Exception e){
            _log.error("Error reading the CSVW content: "+e.getMessage());
        }
    }


}
