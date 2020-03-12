package es.upm.fi.dia.oeg.model;

import org.apache.commons.io.Charsets;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.stream.Collectors;

public class YarrrmlMapping {

    private String content;

    public YarrrmlMapping(String content) {
        this.content = content;
    }

    public YarrrmlMapping(Path path) {
        setContent(path);
    }

    public YarrrmlMapping(URL url) {
        setContent(url);
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public void setContent (Path path){
        try {
            this.content = String.join("\n",Files.readAllLines(path, Charsets.toCharset("UTF-8")));
        }catch (Exception e){
            //ToDo log
        }
    }
    
    public void setContent (URL url){
        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(url.openStream()));
            this.content=reader.lines().collect(Collectors.joining("\n"));

        }catch (Exception e){

        }
    }
}
