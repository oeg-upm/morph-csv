# Motivating example
All the mappings (RML+FnO, R2RML), annotations (CSVW), data, results and queries are available in the folders of this repositories.

## CSV challenges
We identify 7 challenges where an OBDA has to deal with to make an efficient query evaluation of CSVs. Based on our motivating example, in this section we create queries to test each challege and run over our proposal and morph-rdb (in some cases the challenge is focused on the generated schema of the RDB so the queries are in SQL to check if it is resolved or not).

### NS: CSVs do not provide a schema
Query (SQL):
```
DESCRIBE COMMENTS;
```
Results (link: ):
 - morph-csv: 1 PK, 1 FK, 1 INDEX 4 columns (2 VARCHARS, 1 DATE, 1 INT)
 - morph-rdb: 0 PK, 0 FK, 5 columns (5 VARCHARS)

Reason:
The typical OBDA tools don't exploit the information of the mapping to create the schema of the RDB and this may affect the evaluation of queries such as the performance or the number of results

### NN: CSVs are not normalized
Query (SPARQL):
```
select ?comment ?modifiedDate {
	?comment rdf:type schema:SocialMediaPosting;
	   schema:dateModified ?modifiedDate .
}
```
Results (link: ):
 - morph-csv: 7 SPARQL Result-set
 - morph-rdb: 4 SPARQL Results-set

Reason:
The comment have from 0 to N modified dates that in the CSV are in the same column separeted by "-", a normalization to obtain correct values is needed.

### NU: Data may be in a non-uniform format
Query (SPARQL):
```
select ?date where {
	?s rdf:type schema:SocialMediaPosting;
	   schema:dateCreated ?date .
}
```
Results (link: ):
 - morph-csv: 4 SPARQL Results-Sets with date in the form of dd-MM-yyyy 
 - morph-rdb: error (datatype xsd:date is specify in the mapping but VARCHAR is found)

Reason:
The column date from comments.csv is loaded in the RDB like a VARCHAR because its format is not according to SQL date format (DD-MM-YYYY)


### MD: Missing data
Query (SPARQL):
```
select ?email where {
	?s rdf:type schema:Person;
	   schema:email ?email .
}
```
Results (link: ):
 - morph-csv: 4 SPARQL Results-Sets
 - morph-rdb: 4 SPARQL Results-Sets

Reason:
The results are not correct because ontop and morph-rdb can apply transformation functions to the raw data.


### MM: Missing metadata
Query (SPARQL):
```
select ?s ?name where {
	?s rdf:type schema:Person;
		schema:name ?name . 
} 
```
Results (link: ):
 - morph-csv: 4 SPARQL Results-Sets
 - morph-rdb: error

Reason:
The column names are not specific in persons.csv and are needed by typicall OBDA engines to perform the query.

### IJ: Joins are not explicit
Query (SPARQL):
```
select ?commnet ?author where {
	?comment rdf:type schema:SocialMediaPOsting;
		schema:author ?author . 
} 
```
Results (link: ):
 - morph-csv: 4 SPARQL Results-Sets
 - morph-rdb: error

Reason:
It is necessary to apply transformation functions over the raw data to find the join between comments and people. It is not possible to define this functions in R2RML.

### IC: Irrelevant Columns
Query (SQL):
```
DESCRIBE COMMENTS;
```
Results (link:):
 - morph-csv: 4 columns
 - morph-rdb: 5 columns

Reason:
nOfLikes column is not in the mapping so it is not needed to load the column in the RDB.


