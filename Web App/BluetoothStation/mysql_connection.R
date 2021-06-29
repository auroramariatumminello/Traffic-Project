library(odbc)
library(RMySQL)
library(config)
library("RMariaDB")
library(tidyverse)

config <- config::get(file = "config.yml")

dbconnect <- function(){ 
  mydb <- RMariaDB::dbConnect(
    RMariaDB::MariaDB(),
    user = config$db_user,
    password = config$password,
    dbname = config$dbname,
    host = config$db_host
  )
  return(mydb)
}

dbconnect()
