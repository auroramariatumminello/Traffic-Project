#load libraries
library(shiny)
library(leaflet)
#library(dplyr)
library(leaflet.extras)
#import data
#setwd("G:/Il mio Drive/First Year/Big Data Technologies/Traffic Project/Web App/BluetoothStation")
data <- read.csv("BluetoothStations.csv")
# Define UI for application that draws a histogram
ui <- fluidPage(
    tags$style(type = "text/css", "html, body, #map {padding:5px;width:100%;height:100%}"),
    selectInput("station", 
                "Select a station",
                choices = c("All",data$name)),
    leafletOutput(outputId = "map",height=700),
)
# Define server logic required to draw a histogram
server <- function(input, output) {
    
    selected_station = reactive({
        df = data
        if(input$station!='All'){
            df = data[data$name==input$station,]
        }
        df
    })

    output$map <- renderLeaflet({
        leaflet(data) %>% 
            setView(lng = 11.2, lat = 46.40, zoom =9)  %>%
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
