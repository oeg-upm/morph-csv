# Morph-CSV (2.0)



## What is Morph-CSV?

![Morph-csv workflow](figures/architecture.png?raw=true "Morph-CSV workflow")

## How to use it?
We provide two ways to run morph-csv: using the created docker image or directly run with Python3. First of all clone the repository:
```bash
git clone https://github.com/oeg-upm/morph-csv-sparql.git
cd morph-csv-sparql
```
Then choose one of the available options:
- Using docker and docker-compose*:
    ```bash
    docker-compose up -d
    docker exec -it morphcsv ./run-morph-csv.sh -c /configs/config-file.json -q /queries/query-file.rq
    ```

    *If you have any local resource you want to use copy it to the corresponding shared volume (folders: data, mappings, configs or queries)

- Using python3:
    ```bash
    pip3 install -r requirements.txt
    python3 morphcsv.py -c path-to-config-file.json -q path-to-query-file.rq
    ```

### Define your config.json file
```json
{
  "csvw":"PATH OR URL to CSVW annotations",
  "yarrrml": "PATH OR URL TO YARRRML+FnO Mapping"
}
```


## Authors and Contact
Ontology Engineering Group - Data Integration:
- David Chaves-Fraga ([dchaves@fi.upm.es](mailto:dchaves@fi.upm.es))
- Jhon Toledo
- Luis Pozo ([luis.pozo@upm.es](mailto:luis.pozo@upm.es))
- Freddy Priyatna
