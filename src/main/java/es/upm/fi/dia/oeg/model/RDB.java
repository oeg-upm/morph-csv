package es.upm.fi.dia.oeg.model;

import org.apache.commons.io.Charsets;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.file.Files;
import java.nio.file.Path;

public class RDB {
    private static final Logger _log = LoggerFactory.getLogger(RDB.class);
    private String name;
    private String content;

    public RDB(String name, String content) {
        this.name = name;
        this.content = content;
    }

    public RDB(String name, Path path) {
        this.name = name;
        setContent(path);
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public void setContent (Path path){
        try {
            this.content = Files.readAllLines(path, Charsets.toCharset("UTF-8")).toString();
        }catch (Exception e){
           _log.error("Error reading the content of the RDB: "+e.getMessage());
        }
    }


}
