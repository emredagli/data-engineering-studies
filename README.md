# Data Engineering Studies

The workspace contains data engineering projects & studies & notes.

## Projects and Case Studies

This section mainly contains [Data Engineering Nanodegree Program](https://www.udacity.com/course/data-engineer-nanodegree--nd027) notes & projects.

### [Data Modelling with Postgres](project_1_Data_Modelling_with_Postgres)
In the scope of this project we would like analyze data collected from a streaming app. The main focus is understanding songs and users data relations to provide feedback to Analytics Team. 
Since the data are collected into 2 different json datasets it is hard to extract the relation and make query on it. 
A Postgres Analytic database is prepared and a pipeline is implemented to feed this database.

### [Data Modeling with Apache Cassandra](project_2_Data_Modeling_with_Cassandra)
In the scope of this project requirement-based (query-based) Apache Casandra Tables are created and populated for the similar dataset used on previous project.
Step-by-step, [a Jupiter notebook page](project_2_Data_Modeling_with_Cassandra/Apache_Cassandra_Solution_For_Spofity_Project.ipynb) was prepared by solving the tasks given for the project.

### [Data Warehouse with Redshift](project_3_Data_Warehouse_with_Redshift)
In this project a Redshift Cluster was created and an ETL pipeline was build to create the DWH.
* Creating a Redshift Cluster with Terraform,
* Design the DWH with star schema,
* Implement a pipeline to:
  * Extract the data from S3,
  * Stage the extracted data in the Redshift Cluster,
  * Transform the staging data to update the fact table and dimension tables.

[//]: # (### Data Lake Project)

[//]: # ()
[//]: # (### Data Pipelines Project)

### Course Notes

#### [Automate Data Pipelines with Apache Airflow](5_Automate_Data_Pipelines)

[//]: # (#### [Links & Resources]&#40;1_Data_Engineering_Links_And_Resources&#41;)

[//]: # (#### [Data Modeling]&#40;2_Data_Modeling&#41;)

[//]: # (#### [Cloud Data Warehouses]&#40;3_Cloud_Data_Warehouses&#41;)

[//]: # (#### [Spark and Data Lakes]&#40;4_Spark_and_Data_Lakes&#41;)
