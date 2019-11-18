## Completeness of the query evaluation
In this section  we check the number of results of a set of queries over a set of real CSV files. As far as we are aware
of, there are no general-purpose benchmarks in the state of the art for testing our main contributions. Therefore, we 
have created a testbed as follows: 1) we have selected and downloaded a set of CSV files, available 
as open data, from the domain of public transport and general city data; 2) we have he corresponding annotations and mappings 
for morph-csv and the R2RML mappings for morph-rdb and ontop; 3) we have proposed several SPARQL queries that reflect 
real-life queries exploiting this data, with an increasing degree of complexity; 4) we evaluate this queries over
the selected engines and measure the number of responses.

### Queries
| Query  | Description | (# Sources) | FnO(SQL) Trans. func |
| :-------------: | ------------- | :---------: | :---------: |
| Q1  | Stops from different transport with the same name  | 2| 2 basic functions
| Q2  | Stops nearby the museums  | 2 | 4 reg. expressions
| Q3  | Stops nearby the sport centers  | 2 | 4 reg. expressions
| Q4  | Stops from different transports with same name and near a museum| 3 | 4 reg. expressions + 2 basic
| Q5  | Stops nearby museums and sport center  | 3 | 8 reg. expressions


### Results
| Query  | Morph-RDB | Proposal |  
| :-------------: | :-------------: |  :-------------: | 
| Q1  | 45 | 124 
| Q2  | 0 | 21 
| Q3  | 0  | 28  
| Q4  | 0 | 18  
| Q5  | 0  | 17 

We are checking how affects the inclusion of basic transformation functions in real-world CSV and we observe that
state-of-the-art engines are not able to deal with the heterogeneity of this format. We prove that consider this kind
of mappings the completeness of the query is improved.
