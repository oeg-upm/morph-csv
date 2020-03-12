package es.upm.fi.dia.oeg.model;

import es.upm.fi.dia.oeg.rmlc.api.binding.jena.JenaRMLCMappingManager;
import es.upm.fi.dia.oeg.rmlc.api.model.TriplesMap;
import es.upm.fi.dia.oeg.rmlc.api.model.impl.InvalidRMLCMappingException;
import org.apache.commons.io.Charsets;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Collection;
import java.util.Map;

public class RMLCMapping {

    private String content;
    private Collection<TriplesMap> triples;
    private Map<String,String> prefixes;

    public RMLCMapping(String content, Collection<TriplesMap> triples) {
        this.content = content;
        this.triples = triples;
    }

    public RMLCMapping( String content) {
        this.content = content;
        setTriples(content);
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public Collection<TriplesMap> getTriples() {
        return triples;
    }

    public Map<String, String> getPrefixes() {
        return prefixes;
    }

    public void setPrefixes(Map<String, String> prefixes) {
        this.prefixes = prefixes;
    }

    public void setTriples(Collection<TriplesMap> triples) {
        this.triples = triples;
    }

    public void setTriples(String mappingContent) {
        JenaRMLCMappingManager mm = JenaRMLCMappingManager.getInstance();
        Model m = ModelFactory.createDefaultModel();
        m = m.read(new ByteArrayInputStream(mappingContent.getBytes()), null, "TTL");
        prefixes=m.getNsPrefixMap();
        try {
            this.triples = mm.importMappings(m);
        } catch (InvalidRMLCMappingException e) {
            System.out.println("Exception in read mapping: " + e.getMessage());
        }
    }



    public void setContent (Path path){
        try {
            this.content = Files.readAllLines(path, Charsets.toCharset("UTF-8")).toString();
        }catch (Exception e){
            //ToDo log
        }
    }


    public void setContent (URL url){
        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(url.openStream()));
            this.content=reader.lines().toString();

        }catch (Exception e){

        }
    }
}
