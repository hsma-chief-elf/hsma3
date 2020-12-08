library(fitdistrplus)
library(actuar)
library(shiny)

# https://mastering-shiny.org/ for useful tutorials and examples
# https://shiny.rstudio.com/reference/shiny/1.4.0/ for reference materials

ui <- fluidPage(
  titlePanel("HSMA distribution fitting tool"),
  
  sidebarLayout(
    sidebarPanel(),
    mainPanel()
  )
)

server <- function(input, output){}

shinyApp(ui=ui, server=server)

