1) Create ssh session 
2) Move .py files to local fs(scp)
3) In terminal run (python3 --version 3.5.2 or higher): 
	sudo python3 Generator.py 
	sudo hdfs dfs -put tableA.tsv <hdfs_folderA_name>/tableA.tsv 
	sudo hdfs dfs -put tableB.tsv <hdfs_folderB_name>/tableB.tsv
4) Create 2 tables in Hive (use any tool available for you like Ambari hive view or beeline shell)
DDL sripts:

CREATE TABLE `t1`(
  `a` double, 
  `b` string, 
  `c` string, 
  `d` string, 
  `e` string)
ROW FORMAT DELIMITED 
  FIELDS TERMINATED BY '\t' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  '<hdfs_folderA_name>'
TBLPROPERTIES (
  'serialization.null.format'='null'
 )


CREATE TABLE `t2`(
  `a` decimal(27,4), 
  `b` string, 
  `c` string, 
  `d` string, 
  `e` boolean)
ROW FORMAT DELIMITED 
  FIELDS TERMINATED BY '\t' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  '<hdfs_folderB_name>'
TBLPROPERTIES (
  'serialization.null.format'='null'
 )
 
 5) Test data generated. You could query hive tables in order to check data.
 ---------------------------------------------------------------------------------------------------------------------------
 6) In terminal run (python3 --version 3.5.2 or higher): 
	sudo rm -f tableA.tsv | sudo rm -f tableB.tsv
	sudo hdfs dfs -copyToLocal <hdfs_folderA_name>/tableA.tsv tableA.tsv
	sudo hdfs dfs -copyToLocal <hdfs_folderB_name>/tableB.tsv tableB.tsv
	sudo python3 Comparator.py 
 7) Check script output to see if files are identical.
