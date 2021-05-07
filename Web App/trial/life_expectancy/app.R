library(shiny)    # for shiny apps
library(leaflet)  # renderLeaflet function
library(spData)   # loads the world dataset 
library(sf)
ui = bootstrapPage(
    tags$style(type = "text/css", "html, body, #map {padding:5px;width:100%;height:100%}"),
    sliderInput(inputId = "life", 
                "Life expectancy",
                49, 84, 
                value = 80),
    leafletOutput(outputId = "map")
)
server = function(input, output) {
    output$map = renderLeaflet({
        leaflet() %>%
            setView(lng = 11.2, lat = 46.6, zoom = 3)  %>%
            addTiles() %>%
            addPolygons(data = world[world$lifeExp < input$life, ])})
}
shinyApp(ui, server)
