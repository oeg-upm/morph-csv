package es.upm.fi.dia.oeg.rdb;


import es.upm.fi.dia.oeg.model.CSVW;
import es.upm.fi.dia.oeg.rmlc.api.model.TriplesMap;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


import java.io.PrintWriter;
import java.sql.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class RDBConexion {

    private static final Logger _log = LoggerFactory.getLogger(RDBConexion.class);

    private ArrayList<String> foreignkeys;
    private PrintWriter pw;
    private PrintWriter pw2;

    public RDBConexion(String rdb){
        try{
            Class.forName ("org.h2.Driver");
            foreignkeys = new ArrayList<>();
            try {
               pw  = new PrintWriter("output/"+rdb+"-schema.sql", "UTF-8");
               pw2 = new PrintWriter("output/"+rdb+"-inserts.sql","UTF-8");
            }catch (Exception e){

            }
        }catch (Exception e){
            _log.error("The H2 driver has not found");
        }
    }

    public void close(){
        pw.close();pw2.close();
    }

    public void createDatabase(String rdb, String tables){

        try {
            long startTime = System.currentTimeMillis();
            createTables(tables,rdb);
            long stopTime = System.currentTimeMillis();
            long elapsedTime = stopTime - startTime;
            _log.info("The "+rdb+" has been created in H2 successfully in: "+elapsedTime+"ms");
        }catch (Exception e ){
            _log.error("Error connecting with H2: "+e.getMessage());
        }
    }

    private void createTables(String tables, String rdb){
        try {
            Class.forName ("org.h2.Driver");
            Connection c = DriverManager.getConnection("jdbc:h2:./output/"+rdb+";AUTO_SERVER=TRUE", "sa", "");
            Statement s=c.createStatement();
            String[] st = tables.split("\n");
            for(String saux : st) {
                try {
                    if (!saux.matches(".*FOREIGN.*")) {
                        s.execute(saux);
                        pw.println(saux);
                        //System.out.println(saux);
                    } else {
                        String tableName = saux.split("TABLE")[1].split("\\(")[0];
                        String[] splitedst = saux.split("FOREIGN");
                        for (int i = 1; i < splitedst.length; i++) {
                            if (splitedst[i].matches(".*,")) {
                                foreignkeys.add("ALTER TABLE " + tableName + " ADD FOREIGN " + splitedst[i].replace(",", ";"));
                            } else {
                                foreignkeys.add("ALTER TABLE " + tableName + " ADD FOREIGN " + splitedst[i].replace(");", ";"));
                            }
                        }
                        s.execute(splitedst[0].substring(0, splitedst[0].length() - 1) + ");");
                        pw.println(splitedst[0].substring(0, splitedst[0].length() - 1) + ");");
                        //System.out.println(splitedst[0].substring(0,splitedst[0].length()-1)+");");
                    }
                }catch (SQLException e){
                    _log.error("Error creating the table "+saux+" in "+rdb+":"+e.getMessage());
                }
            }
            s.close();c.close();

        }catch (Exception e){
            _log.error("Error open the connection for  "+rdb+": "+e.getMessage());
        }
    }

    public void loadCSVinTable(TriplesMap tp, List<String[]> rows, String table, String rdb, CSVW csvw){
        try {

            Class.forName ("org.h2.Driver");
            Connection c = DriverManager.getConnection("jdbc:h2:./output/"+rdb+";AUTO_SERVER=TRUE", "sa", "");

            //String inserts="",totalInserts="";
            _log.info("Executing inserts for table: "+table);
            long startTime = System.currentTimeMillis();
            List<String[]> rowsWithoutHeader = rows.subList(1,rows.size());
            ExecutorService exec = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
            try {
                for (final Object o : rowsWithoutHeader) {
                    exec.submit(new Runnable() {
                        @Override
                        public void run() {

                            // do stuff with o.
                            String[] r = (String[]) o;
                            StringBuilder insert = new StringBuilder();
                            insert.append("INSERT INTO "+table+" ");
                            insert.append("VALUES(");
                            for(int j=0;j<r.length;j++){
                                if(RDBUtils.checkColumnInAnnotations(rows.get(0)[j],tp,csvw))
                                    if(r[j].equals("")){
                                        insert.append("'',");
                                    }
                                    else if(r[j].equals("NULL")){
                                        insert.append("NULL,");
                                    }
                                    else {
                                        insert.append("'" + r[j].replace("'","''") + "',");
                                    }
                            }
                            String e = insert.substring(0,insert.length()-1)+");";

                            try {
                                c.createStatement().execute(e);
                                pw2.println(e);
                            }catch (SQLException exception){
                                _log.error("Error inserting the instances: "+exception.getLocalizedMessage());
                            }
                        }
                    });
                }
            } finally {
                exec.shutdown();
            }

            try {
                exec.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);

            } catch (InterruptedException e) {
                _log.error("Error waiting for indexing of the instances of "+table+": "+e.getLocalizedMessage());
            }
            long stopTime = System.currentTimeMillis();
            long elapsedTime = stopTime - startTime;
            _log.info("The instances of "+table+" have been indexed in H2 successfully in: "+elapsedTime+"ms");

           /* for(int i=1; i<rows.size();i++){
                StringBuilder insert = new StringBuilder();
                insert.append("INSERT INTO "+table+" ");
                insert.append("VALUES(");
                for(int j=0;j<rows.get(i).length;j++){
                    if(RDBUtils.checkColumnInMapping(rows.get(0)[j],tp))
                        if(rows.get(i)[j].equals("")){
                            insert.append("'',");
                        }
                        else if(rows.get(i)[j].equals("NULL")){
                            insert.append("NULL,");
                        }
                        else {
                            insert.append("'" + rows.get(i)[j].replace("'","''") + "',");
                        }
                }
                String exec = insert.substring(0,insert.length()-1)+");\n";
                inserts+=exec;
                if(i%5000==0){
                    _log.info("Inserting 5000 instances in "+table+"...");
                    totalInserts += inserts;
                    long startTime = System.currentTimeMillis();
                    s.execute(inserts);
                    long stopTime = System.currentTimeMillis();
                    long elapsedTime = stopTime - startTime;
                    _log.info("The instances have been indexed in H2 successfully in: "+elapsedTime+"ms");
                    inserts="";
                }
                //System.out.println(exec);
            }
            _log.info("Inserting last instances in "+table+"...");
            long startTime = System.currentTimeMillis();
            s.execute(inserts);
            long stopTime = System.currentTimeMillis();
            long elapsedTime = stopTime - startTime;
            _log.info("The instances have been indexed in H2 successfully in: "+elapsedTime+"ms");
            totalInserts+=inserts;
             startTime = System.currentTimeMillis();
            pw2.println(totalInserts);
            stopTime = System.currentTimeMillis();
            elapsedTime = stopTime - startTime;
            _log.info("The instances have been printed at output file in: "+elapsedTime+"ms");*/


        }catch (Exception e){
            _log.error("Error creating the tables in the rdb "+rdb+": "+e.getMessage());
        }
    }

    public void addForeignKeys(String rdb){
        try {
            Class.forName("org.h2.Driver");
            Connection c = DriverManager.getConnection("jdbc:h2:./output/" + rdb+";AUTO_SERVER=TRUE", "sa", "");
            Statement s = c.createStatement();
            for(String f: foreignkeys) {
                try {
                    s.execute(f);
                    pw.println(f);
                }catch (SQLException e){
                    _log.error("Error creating a FK: "+e.getLocalizedMessage());
                }
            }
        }catch (Exception e){
            _log.error("Error connecting to the database "+rdb+": "+e.getMessage());
        }
    }


    public void updateDataWithFunctions (HashMap<String,HashMap<String,String>> functions, String rdb, boolean index){
        long startTime = System.currentTimeMillis();
        try {
            Connection c = DriverManager.getConnection("jdbc:h2:./output/"+rdb+";AUTO_SERVER=TRUE", "sa", "");
            Statement s = c.createStatement();
            for(Map.Entry<String,HashMap<String,String>> entry : functions.entrySet()){
                String table_name = entry.getKey();
                HashMap<String,String> column_function = entry.getValue();
                for(Map.Entry<String,String> function_entry : column_function.entrySet()){
                    String alter_column = function_entry.getKey();
                    String function_exp = function_entry.getValue().replace("{","").replace("}","");
                    //if(function_exp.matches(".*\\(.*")) {
                    try {
                        s.execute("ALTER TABLE " + table_name + " ADD " + alter_column + ";");
                        pw.println("ALTER TABLE " + table_name + " ADD " + alter_column + ";");
                        //System.out.println("ALTER TABLE " + table_name + " ADD " + alter_column + ";");
                        s.execute("UPDATE " + table_name + " SET " + alter_column.split(" ")[0] + "=" + function_exp + ";");
                        pw2.println("UPDATE " + table_name + " SET " + alter_column.split(" ")[0] + "=" + function_exp + ";");
                        //System.out.println("UPDATE " + table_name + " SET " + alter_column.split(" ")[0] + "=" + function_exp + ";");
                        //}
                        if (index) {
                            s.execute("CREATE INDEX " + alter_column.split(" ")[0] + "s ON " + table_name + " (" + alter_column.split(" ")[0] + ")");
                            pw.println("CREATE INDEX " + alter_column.split(" ")[0] + "s ON " + table_name + " (" + alter_column.split(" ")[0] + ");");
                            //System.out.println("CREATE INDEX "+alter_column.split(" ")[0]+"s ON "+table_name+" ("+alter_column.split(" ")[0]+")");
                        }
                    }catch (SQLException e){
                        _log.error("Error creating index: "+e.getLocalizedMessage());
                    }

                }
            }
            s.close();c.close();

        }catch (Exception e){
            _log.error("Error in update the table: "+e.getMessage());
        }
        long stopTime = System.currentTimeMillis();
        long elapsedTime = stopTime - startTime;
        _log.info("The "+rdb+" has been updated in H2 successfully in: "+elapsedTime+"ms");
    }
}
