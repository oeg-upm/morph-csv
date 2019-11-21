# Morph-CSV (2.0)
SPARQL query guide for enhancing virtual KG access over tabular open data 


## What is Morph-CSV?


## How to use it?
We provide two ways to run morph-csv: using the created docker image or directly run with Python3. First of all clone the repository:
```bash
git clone https://github.com/oeg-upm/morph-csv-sparql.git
cd morph-csv-sparql
```
The choose one of the available options:
- Using docker and docker-compose*:
    ```bash
    docker-compose up -d
    docker exec -it 'run-morph-csv.sh -c /configs/config-file.json -q /queries/query-file.rq' morphcsv
    ```

    *If you have any local resource you want to use copy it to the corresponding shared volume (folders: data, mappings, configs or queries)

- Using python3:
    ```bash
    pip3 install -r requirements.txt
    python3 morphcsv.py -c path-to-config-file.json -q path-to-query-file.rq
    ```

## Scientific Contributions


## Authors and Contact
Ontology Engineering Group - Data Integration:
- David Chaves-Fraga
- Jhon Toledo
- Luis del Pozo
- Freddy Priyatna