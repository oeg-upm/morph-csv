package es.upm.fi.dia.oeg.utils;


import org.apache.commons.cli.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class CommandLineProcessor {
    private static final Logger log = LoggerFactory.getLogger(CommandLineProcessor.class);
    private static final Options cliOptions = generateCLIOptions();



    public static CommandLine parseArguments(String[] args) {
        CommandLineParser cliParser = new DefaultParser();
        CommandLine commandLine = null;
        try{
            commandLine=cliParser.parse(getCliOptions(), args);
        }catch (ParseException e){
            log.error("Error parsing the command line options: "+e.getMessage());
        }
        return commandLine;
    }


    private static Options generateCLIOptions() {
        Options cliOptions = new Options();

        cliOptions.addOption("h", "help", false,
                "show this help message");
        cliOptions.addOption("q", "query file", true,
                "URI or path to query file (required)");
        cliOptions.addOption("c", "config file", true,
                "URI or path to the config file (required");
        cliOptions.addOption("e", "engine (morph default)", true,
                "Engine to choose (ontop/morph)");


        return cliOptions;
    }

    public static Options getCliOptions() {
        return cliOptions;
    }

    public static void displayHelp() {
        HelpFormatter formatter = new HelpFormatter();
        formatter.printHelp("RMLC: RDF Mapping Language for heterogeneous CSV files", getCliOptions());
        System.exit(1);
    }
}