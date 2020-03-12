# Morph-CSV
## How to enhance OBDA query-translation over Tabular Open Data?

Use CSVW annotations and RML FnO mappings (following YARRRML spec) to generate R2RML mappings and an enriched RDB to enhance OBDA query translation over Tabular Open Data (CSV) files. This framework can be embedded in the top of any R2RML-compliant engine.

- Docker image: https://hub.docker.com/r/dchaves1/morph-csv

### How it works?
![Morph-csv workflow](figures/morphcsv.png?raw=true "Morph-CSV workflow")

## How to run it?
Using the example of our last tutorial at ESWC2019 - Virtual Knowledge Graph Generation (https://tutorials.oeg-upm.net/vkg2019/)
```bash
git clone https://github.com/oeg-upm/vkg-tutorial-eswc2019
cd vkg-tutorial-eswc2019/morph-csv
docker-compose up -d
cd run-scripts
./run-XXX
```


## Examples:
At the evaluation folder you find original data, mappings, queries and results of 4 examples:
- Comments and persons (at motivating-example folder)
- Linking Open City data (at open-city-data-validation folder)
- Virtual Bio2RDF (at bio2rdf folder)
- Performance over GTFS transport data (at transport-performance folder)

## Publications:
-  David Chaves-Fraga, Freddy Priyatna, Idafen Santana-Pérez and Oscar Corcho  “Virtual Statistics Knowledge Graph Generation from CSV files”. In:Emerging Topics in Semantic Technologies: ISWC2018  Satellite  Events. Vol. 36. Studies on the Semantic Web. IOS Press,2018, pp. 235–244 [Online Version](https://www.researchgate.net/publication/328118582_Virtual_Statistics_Knowledge_Graph_Generation_from_CSV_files)
- Oscar Corcho, Freddy Priyatna, David Chaves-Fraga: "Towards a New Generation of Ontology Based Data Access". In: Semantic Web Journal, 2019. [Preprint version](http://www.semantic-web-journal.net/content/towards-new-generation-ontology-based-data-access)
- Ana Iglesias-Molina, David Chaves-Fraga, Freddy Priyatna, Oscar Corcho: "Enhancing the Maintainability of the Bio2RDF project Using Declarative Mappings". In: 12th International Semantic Web Applications and Tools for Health Care and Life Sciences Conference, 2019.
