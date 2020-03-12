package es.upm.fi.dia.oeg.model;


import es.upm.fi.dia.oeg.rdb.CSVWUtils;
import es.upm.fi.dia.oeg.rmlc.api.model.Source;
import es.upm.fi.dia.oeg.rmlc.api.model.TriplesMap;
import org.json.JSONArray;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.net.MalformedURLException;
import java.net.URL;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collection;

public class Dataset {

    private CSVW csvw;
    private YarrrmlMapping yarrrmlMapping;
    private RMLCMapping rmlcMappingY;
    private RMLCMapping rmlcMappingC;
    private ArrayList<CSV>  csvFiles;
    private String r2rmlMapping;
    private RDB rdb;
    private static final Logger _log = LoggerFactory.getLogger(Dataset.class);


    public Dataset (String rdbName){
        rdb = new RDB(rdbName,"");
    }

    public Dataset (CSVW csvw, YarrrmlMapping yarrrmlMapping){
        this.yarrrmlMapping = yarrrmlMapping;
        this.csvw = csvw;
    }

    public Dataset(String csvw, String yarrrmlMapping){
        try {
            if (csvw.matches("http[s]://.*")) {
                URL url = new URL(csvw);
                this.csvw = new CSVW(url);
            } else {
                Path p = Paths.get(csvw);
                this.csvw = new CSVW(p);
            }
            if (yarrrmlMapping.matches("http[s]://.*")) {
                URL url = new URL(yarrrmlMapping);
                this.yarrrmlMapping = new YarrrmlMapping(url);
            } else {
                Path p = Paths.get(yarrrmlMapping);
                this.yarrrmlMapping = new YarrrmlMapping(p);
            }
        }catch (MalformedURLException e){

        }
        csvFiles = new ArrayList<>();
    }

    public CSVW getCsvw() {
        return csvw;
    }

    public void setCsvw(CSVW csvwFile) {
        this.csvw = csvwFile;
    }

    public YarrrmlMapping getYarrrmlMapping() {
        return yarrrmlMapping;
    }

    public void setYarrrmlMapping(YarrrmlMapping yarrrmlMapping) {
        this.yarrrmlMapping = yarrrmlMapping;
    }

    public RMLCMapping getRmlcMappingY() {
        return rmlcMappingY;
    }

    public void setRmlcMappingY(RMLCMapping rmlcMappingY) {
        this.rmlcMappingY = rmlcMappingY;

        setCsvFiles(this.rmlcMappingY.getTriples());
    }

    public RMLCMapping getRmlcMappingC() {
        return rmlcMappingC;
    }

    public void setRmlcMappingC(RMLCMapping rmlcMappingC) {
        this.rmlcMappingC = rmlcMappingC;
    }

    public ArrayList<CSV> getCsvFiles() {
        return csvFiles;
    }

    public void setCsvFiles(ArrayList<CSV> csvFiles) {
        this.csvFiles = csvFiles;
    }

    public void setCsvFiles(Collection<TriplesMap> tripleMaps) {
        if(csvFiles==null){
            csvFiles = new ArrayList<>();
        }
        _log.info("Loading the CSV source files");
        tripleMaps.forEach(tripleMap -> {
            String logicalSource=((Source)tripleMap.getLogicalSource()).getSourceName();
            String name = (logicalSource.split("/"))[(logicalSource.split("/")).length-1].replace(".csv","");
            JSONObject annotations = CSVWUtils.getCSVWFromSource(csvw.getContent().getJSONArray("tables"),logicalSource);
            JSONObject dialect =null;
            if(annotations!=null && annotations.has("dialect")) {
                dialect = annotations.getJSONObject("dialect");
            }
            if(logicalSource.matches("http[s]://.*")){
                try {
                    csvFiles.add(new CSV(name, logicalSource, new URL(logicalSource),dialect));
                }catch (MalformedURLException e){
                    _log.error("Error reading the URL for the CSV "+name+".csv: "+e.getLocalizedMessage());
                }
            }
            else {
                csvFiles.add(new CSV(name,logicalSource,Paths.get(logicalSource),dialect));
            }

        });
    }

    public String getR2rmlMapping() {
        return r2rmlMapping;
    }

    public void setR2rmlMapping(String r2rmlMapping) {
        this.r2rmlMapping = r2rmlMapping;
    }

    public RDB getRdb() {
        return rdb;
    }

    public void setRdb(RDB rdb) {
        this.rdb = rdb;
    }
}
