library(fitdistrplus)
library(actuar)
library(shiny)

# https://mastering-shiny.org/ for useful tutorials and examples
# https://shiny.rstudio.com/reference/shiny/1.4.0/ for reference materials

ui <- fluidPage(
  titlePanel("HSMA distribution fitting tool"),
  
  sidebarLayout(
    sidebarPanel(
      h3(),
      fileInput(),
      br(),
      h3(),
      selectInput(),
      checkboxInput(),
      checkboxInput()
    ),
    mainPanel(
      tabsetPanel(type="tabs",
                  tabPanel(),
                  tabPanel(),
                  tabPanel())
    )
  )
)

server <- function(input, output){
  my_data <- reactive({
    return()
  })
  
  fitting <- reactive({
    return()
  })
  
  output$dataTable <- renderTable({})
  output$empDen <- renderPlot({
    data <- my_data()
    })
  output$cfPlot <- renderPlot({})
  output$cfSummary <- renderPrint({})
  
  output$fitSummary <- renderPrint({
  })
  
  output$denPlot <- renderPlot({
    })
  
  output$cumluPlot <- renderPlot({
    })
  
  output$qqPlot <- renderPlot({
    })
  
  output$ppPlot <- renderPlot({
    })
  
  output$goodSummary <- renderPrint({
    })
  
  output$bootSummary <- renderPrint({
    })
}

shinyApp(ui=ui, server=server)

