#load libraries
library(shiny)
library(leaflet)
#library(dplyr)
library(leaflet.extras)
#import data
data <- read.csv("BluetoothStations.csv")

# Define UI for application that draws a histogram
ui <- bootstrapPage(
    tags$style(type = "text/css", "html, body {width:100%;height:100%}"),
    leafletOutput("map", width = "100%", height = "100%"),
    
)
# Define server logic required to draw a histogram
server <- function(input, output) {

    output$map <- renderLeaflet({
        leaflet(data) %>% 
            setView(lng = 11.2, lat = 46.6, zoom = 9)  %>%
            addTiles() %>% 
            addMarkers(data = data, 
                       lat = ~ lat,
                       lng = ~ lon, 
                       popup = ~as.character(name), 
                       label = ~as.character(paste0("Name: ", sep = " ", name)))
    })
}

# Run the application 
shinyApp(ui = ui, server = server)
