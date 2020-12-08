library(shiny)

ui <- fluidPage(
  titlePanel("My first web app"),
  
  sidebarLayout(
    sidebarPanel(
      h3("A sidebar panel"),
      p("In the side bar I can place
        all of my input selection options
        for what I want to happen in the
        main panel"),
    sliderInput("obs",
                "Number of observations:",
                min=0,
                max=1000,
                value=500)
    ),
    mainPanel(
      h3("The main panel"),
      p("In the main panel I would place
        all of my outputs which change
        given the inputs in the sidebarPanel"),
      plotOutput("distPlot")
    )
  )
)

server <- function(input, output){
  output$distPlot <- renderPlot({hist(rnorm(input$obs))})
}

shinyApp(ui=ui, server=server)