package es.upm.fi.dia.oeg.model;

import org.apache.commons.io.Charsets;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.file.Files;
import java.nio.file.Path;
public class R2RMLMapping {
    private static final Logger _log = LoggerFactory.getLogger(R2RMLMapping.class);
    private String mappingName;
    private String content;

    public R2RMLMapping(String mappingName, String content) {
        this.mappingName = mappingName;
        this.content = content;
    }


    public String getMappingName() {
        return mappingName;
    }

    public void setMappingName(String mappingName) {
        this.mappingName = mappingName;
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
            _log.error("Error reading the content of the R2RML mapping: "+e.getMessage());
        }
    }

}
