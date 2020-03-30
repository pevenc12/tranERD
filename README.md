# TranERD

## Intoduction

This work aims to map **ER model** and **relational database** to each other through the help of XML file. Moreover, one can perform a **lightweight** query which prunes the database and let the database be visualized in the format of ER diagram.

## Prerequisite

You must install **python3**.

## Usage
1. Reconstruct the data using XML. In here we take test/MLB.xml as an example.
2. Run **convertor.py**. Then you will see ```YTDB> ``` as command line.
3. Parse the data.
```
parse MLB.xml
```
4. Perform database manipulation.
+ query certain relationship of current database and prune
```python
YTDB> query -r Sponse    # query only the entities and relationships that are related to Sponse
```
+ query certain attribute of current database and prune
```python
YTDB> query -a Address   # query all entities that conatain the "Address" attribute
```
+ translate current database into .sql file
```python
YTDB> transql demo.sql   # demo.sql  will be the output file
```
+ visualize current database by .png file
```python
YTDB> tranERD            # export a demo.png file
```

## Details

Please refer to Report.pdf