# Traffic-Project

## Our aim

The purpose of our project was to design and implement a big data system able to predict in near-time the traffic associated with specific and crucial points of interest monitored by Bluetooth sensors in the Bolzano area, using Open Data Hub Südtirol databases.

## Basic structure of the repository

Sections:

1. Code: all folders and files involved
2. Action: there are two different workflows, the first one (i.e real time data collection)regards the download_real_time script while the second one (i.e model prediction)regards the loop prediction script.
3. Packages: "bdt_new" is a package cointaining docker images of RDS MySQL database, Python and R files.
 
## How to execute specific stages of the pipeline

### Data collection

Data collection is handled by two different scripts:

- `download_history`, locally executed in order to get data in batch;
- `download_real_time`, whose execution is driven by Github Actions by installing requirements and showing some logs inside the specific build (in particular, inside the step "execute script"). It is scheduled to be executed every 30 minutes, since publishers release data every 10 minutes. 

All requirements for both scripts are contained inside `py/download_requirements.txt`. 

`BluetoothStation` script contains three classes that describe three abstract objects: Bluetooth Station, with its geographical coordinates, described by the class Position; Measurement, which considers timestamp, Bluetooth Station and count of vehicles passing. 

### Data ingestion

`DatabaseManager` script instead offers a variety of database managers, depending on the provider. The most basic one is a local MySQL database, the following one is still a MySQL database, but hosted on Amazon RDS (remote connection), whose connection is available through secret credentials. In the end, a simple MongoDB manager was created to insert and delete many observations in a row inside the collection. 

Inside the `db` folder, it is possible to find several scripts for emulating the construction of MySQL database:

- `bluetooothstations.sql` contains the creation schema of all tables inside the db;
- `time_group.sql` and `traffic_per_hour.sql`describe the creation of two summary tables used to query efficiently the database inside the application. 
- all the triggers specified are necessary to update sum and averages inside the previous two tables whenever new observations are inserted in the Database. 

### Model

`Traffic-Bolzano.ipynb` specific notebook for the training phase of the model. In order to run it, it is necessary to use [Databricks](https://databricks.com/), that exploits Spark to handle the massive amount of data for the training phase. 

`Traffic_Loop.py` script aims to continuosly predict the traffic for every station, considering the latest two hours of data at the start and then concatenating results till they get to the current timestamp. The entire workflow is handled through GitHub Actions. Requirements for this script are contained inside the `py/model_requirements.py`. 

Model structure and weights are saved inside `data/model` directory. They were initially exported from the training phase in json and h5 format and then imported inside the loop and continuously updated. 

### Web Application

Inside `Shiny Bolzano Application`, it is possibile to find the original scripts, for both configuration and running, used to build the web application hosted on Shiny Server at the following [link](https://traffic-bolzano.shinyapps.io/traffic-bolzano2/).

`db_connection.R` is the script that contains two functions to connect the application directly to MySQL and MongoDB databases, whereas `Traffic-Bolzano.Rmd` is the actual application written in RMarkdown with the help of shiny and flexdashboard. 

