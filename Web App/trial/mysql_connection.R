library(odbc)
library(RMySQL)
library(config)
library("RMariaDB")
library(tidyverse)

config <- config::get(file = "config.yml")

dbconnect <- function(){ 
  mydb <- RMariaDB::dbConnect(
    RMariaDB::MariaDB(),
    user = "marshall",
    password = "happyslashgiving",
    dbname = "bluetoothstations",
    host = "traffic-db.ce2ieg6xrefy.us-east-2.rds.amazonaws.com"
  )
  return(mydb)
}
