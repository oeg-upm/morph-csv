package es.upm.fi.dia.oeg.translation;

import es.upm.fi.dia.oeg.model.CSVW;
import es.upm.fi.dia.oeg.model.RMLCMapping;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.stream.Collectors;

public class CSVW2RMLC {


    //call api with the link return RMLCMapping

    public static RMLCMapping translateCSVW2RMLC(CSVW csvwAnnotation){
        String rmlcContent ="";

        try {
            rmlcContent = CSVW2RMLC.sendGet(csvwAnnotation.getUrl());
        }catch (Exception e){

        }
        RMLCMapping mapping = new RMLCMapping(rmlcContent);
        return mapping;
    }

    private static String sendGet(String csvwUrl) throws Exception {

        String url = "http://localhost:5002/csvw2rmlc?csvw_url="+csvwUrl;

        URL obj = new URL(url);
        HttpURLConnection con = (HttpURLConnection) obj.openConnection();

        // optional default is GET
        con.setRequestMethod("GET");


        int responseCode = con.getResponseCode();
        System.out.println("\nSending 'GET' request to URL : " + url);
        System.out.println("Response Code : " + responseCode);

        BufferedReader in = new BufferedReader(
                new InputStreamReader(con.getInputStream()));
        String response=in.lines().collect(Collectors.joining("\n"));
        in.close();
        return response;

    }

}
