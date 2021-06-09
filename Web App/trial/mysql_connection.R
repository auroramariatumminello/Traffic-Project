library(odbc)
library(RMySQL)
library(config)

config <- config::get(file = "config.yml")
con <- RMySQL::dbConnect(
  RMySQL::MySQL(),
  user = config$db_user,
  password = config$db_password,
  dbname = config$db_name,
  host = config$db_host
)

df <- con %>%
  dplyr::tbl("station") %>%
  dplyr::collect()