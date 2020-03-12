package es.upm.fi.dia.oeg.model;


import com.univocity.parsers.csv.*;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.net.URL;
import java.nio.file.Path;
import java.util.List;

public class CSV {
    private static final Logger _log = LoggerFactory.getLogger(CSV.class);
    private String nameFile;
    private String url;
    private String parentUrl;
    private CsvParser parser;
    private List<String[]> rows;

    public CSV(String nameFile,String url, CsvParser parser) {
        this.nameFile = nameFile;
        this.url = url;
        this.parser = parser;
    }

    public CSV(String nameFile, String url, Path csv, JSONObject dialect) {
        this.nameFile = nameFile;
        this.url = url;
        setRows(csv,dialect);
    }

    public CSV(String nameFile, List<String[]> rows){
        this.nameFile =nameFile;
        this.rows = rows;
    }

    public CSV(String nameFile,String url, String parentUrl, List<String[]> rows){
        this.nameFile =nameFile;
        this.url = url;
        this.parentUrl = parentUrl;
        this.rows = rows;
    }


    public CSV(String nameFile, String url, URL csv,JSONObject dialect) {
        this.nameFile = nameFile;
        this.url = url;
        setRows(csv,dialect);
    }

    public String getNameFile() {
        return nameFile;
    }

    public void setNameFile(String nameFile) {
        this.nameFile = nameFile;
    }

    public List<String[]> getRows() {
        return rows;
    }

    public String getParentUrl() {
        return parentUrl;
    }

    public void setParentUrl(String parentUrl) {
        this.parentUrl = parentUrl;
    }

    public void setRows (List<String[]> rows){
        this.rows = rows;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public void setRows (Path csv, JSONObject dialect){
        CsvParserSettings settings = this.generateSettings(dialect);
        try {
            this.parser = new CsvParser(settings);
            this.rows = parser.parseAll(new BufferedReader(new FileReader(csv.toAbsolutePath().toString())));
            changeEmptyValues();
        } catch (IOException e) {
           _log.error("Error parsing the CSV "+csv.getFileName()+".csv: "+e.getMessage());
        }
    }

    public void setRows (URL url,JSONObject dialect){
        CsvParserSettings settings = generateSettings(dialect);
        try {
            this.parser = new CsvParser(settings);
            this.rows = this.parser.parseAll(new BufferedReader(new InputStreamReader(url.openStream())));
            changeEmptyValues();
        } catch (IOException e) {
            _log.error("Error parsing the CSV "+url.getFile()+": "+e.getMessage());
        }
    }

    private CsvParserSettings generateSettings(JSONObject dialect){
        CsvParserSettings settings = new CsvParserSettings();
        if(dialect!=null) {
            if(dialect.has("delimiter"))
                settings.getFormat().setDelimiter(dialect.getString("delimiter"));
            if(dialect.has("skipRows"))
                settings.setNumberOfRowsToSkip(Integer.parseInt(dialect.getString("skipRows")));
        }
        settings.setEmptyValue("");
        return settings;
    }

    private void changeEmptyValues(){

        for(int j =0; j<rows.size();j++){
            for(int i=0; i<rows.get(j).length;i++){
                if(rows.get(j)[i]==null){
                    rows.get(j)[i]="";
                }
            }
        }
    }

}
