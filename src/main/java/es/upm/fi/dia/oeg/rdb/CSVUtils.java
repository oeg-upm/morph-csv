package es.upm.fi.dia.oeg.rdb;


import org.apache.xerces.impl.xpath.regex.RegularExpression;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class CSVUtils {


    public static List<String[]> generateCSVfromSeparator(String separator, String column, List<String[]> csv){

        String[] headers = csv.get(0);
        List<String[]> separatedCSV = new ArrayList<>();
        separatedCSV.add(new String[]{"id", column});
        Integer index = getIndexColumnFromHeader(headers,column);
        Integer id =0;
        for (int i=1;i<csv.size();i++){
            String[] data = csv.get(i)[index].split(separator);
            if(data.length>0 && !data[0].equals("NULL")) {
                for (String d : data) {
                    separatedCSV.add(new String[]{Integer.toString(id), d});
                }
                id++;
            }

        }


        return separatedCSV;
    }

    public static List<String[]> removeSeparetedColumn(String column, List<String[]> csv){
        String[] headers = csv.get(0);
        List<String[]> cleanedCSV = new ArrayList<>();
        Integer index= getIndexColumnFromHeader(headers,column);
        Integer fkid=0;
        for(int i=0; i<csv.size() ;i++){
            String[] row = csv.get(i);
            if(i!=0) {
                if(!row[index].equals("NULL")) {
                    row[index] = Integer.toString(fkid);
                    fkid++;
                }
            }
            else {
                row[index] = row[index]+"_J";
            }
            cleanedCSV.add(row);
        }
        return  cleanedCSV;
    }

    public static void changeFormat(String column, List<String[]> csv, JSONObject annotations){

        Integer index = getIndexColumnFromHeader(csv.get(0),column);
        if(index!=null) {
            String format = annotations.getJSONObject("datatype").getString("format");
            Integer yearIndex = null, monthIndex = null, dayIndex = null;
            for (int i = 0; i < format.toCharArray().length; i++) {
                if (yearIndex == null && format.toCharArray()[i] == 'y') {
                    yearIndex = i;
                }
                if (monthIndex == null && format.toCharArray()[i] == 'M') {
                    monthIndex = i;
                }
                if (dayIndex == null && format.toCharArray()[i] == 'd') {
                    dayIndex = i;
                }
            }
            for (int j = 1; j < csv.size(); j++) {
                if (!csv.get(j)[index].equals("NULL") & !csv.get(j)[index].equals("") ) {
                    char[] date = csv.get(j)[index].toCharArray();
                    String year = "", month = "", day = "";
                    for (Integer i = 0; i < date.length; i++) {
                        if (i == yearIndex) {
                            year = getPieceofDate(i, 4, date);
                        }

                        if (i == monthIndex) {
                            month = getPieceofDate(i, 2, date);
                            if (month.toCharArray().length < 2) {
                                month = "0" + month;
                            }
                        }
                        if (i == dayIndex) {
                            day = getPieceofDate(i, 2, date);
                            if (day.toCharArray().length < 2) {
                                day = "0" + day;
                            }
                        }
                    }
                    csv.get(j)[index] = year + "-" + month + "-" + day;
                }
            }
        }

    }

    private static String getPieceofDate(Integer index, int max, char[] date){

        StringBuilder aux = new StringBuilder();
        Integer size=0;
        while(index<date.length && Character.toString(date[index]).matches("\\d") && size<max){
            aux.append(date[index]);
            index++;
            size++;
        }
        return aux.toString();
    }

    public static void putNull(List<String[]> csv, JSONObject annotations){
        String column = CSVWUtils.getTile(annotations);
        Integer index = getIndexColumnFromHeader(csv.get(0),column);
        if(index!=null) {
            for (int i = 1; i < csv.size(); i++) {
                if (csv.get(i)[index].equals(annotations.getString("null"))) {
                    csv.get(i)[index] = "NULL";
                }
            }
        }
    }

    public static void putDefault(List<String[]> csv, JSONObject annotations){
        String column = CSVWUtils.getTile(annotations);
        Integer index = getIndexColumnFromHeader(csv.get(0),column);
        for(int i=1; i<csv.size();i++) {
            if (csv.get(i)[index].equals("")) {
                csv.get(i)[index] = annotations.get("default").toString();
            }
        }
    }

    private static Integer getIndexColumnFromHeader(String[] headers, String column){
        Integer index =null;
        for(int i=0; i<headers.length;i++){
            if(headers[i].trim().equals(column.trim())){
                index = i;
            }

        }
        return index;
    }
}
