library(odbc)
library(RMySQL)
library(config)
library(tidyverse)


setwd("C:/Users/auror/OneDrive/Documenti/GitHub/traffic/Traffic Project/Web App/trial")
config <- config::get(file = "config.yml")
print(config)
mydb <- RMySQL::dbConnect(
  RMySQL::MySQL(),
  user = "marshall",
  password = "happyslashgiving",
  dbname = "bluetoothstations",
  host = "traffic-db.ce2ieg6xrefy.us-east-2.rds.amazonaws.com"
)

query = paste("
              SELECT *
              FROM bluetoothstations.measurement
              ORDER BY timestamp DESC")
rs = dbSendQuery(mydb,query)
rs
