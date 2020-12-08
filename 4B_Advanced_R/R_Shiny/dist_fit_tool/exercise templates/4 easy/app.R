library(fitdistrplus)
library(actuar)
library(shiny)

# https://mastering-shiny.org/ for useful tutorials and examples
# https://shiny.rstudio.com/reference/shiny/1.4.0/ for reference materials

ui <- fluidPage(
  titlePanel("HSMA distribution fitting tool"),
  
  sidebarLayout(
    sidebarPanel(
      h3("Step 1 upload your data"),
      fileInput("","",
                accept=c("text/csv",
                         "text/comma-separated-values,text/plain",
                         ".csv")
                ),
      br(),
      h3("Step 2 select distributions to fit"),
      selectInput("","",
                  multiple=TRUE,
                  choices=c("exp",
                            "lnorm","norm",
                            "pois","weibull",
                            "nbinom","gamma")),
      checkboxInput("", ""),
      checkboxInput("", "")
    ),
    mainPanel(
      tabsetPanel(type="tabs",
                  tabPanel("",
                           h3("Data description"),
                           plotOutput(""),
                           h3("Cullen and Frey graph"),
                           plotOutput(""),
                           h3("Density, cumulative density, QQ and PP plots"),
                           plotOutput(""),
                           plotOutput(""),
                           plotOutput(""),
                           plotOutput("")),
                  tabPanel("Tables",
                           h3("Cullen and Frey summary"),
                           verbatimTextOutput(""),
                           h3("Fit summary"),
                           verbatimTextOutput(""),
                           h3("Goodness of fit summary"),
                           verbatimTextOutput(""),
                           h3("Uncertainty estimates"),
                           verbatimTextOutput("")),
                  tabPanel("Data",
                           h3("Raw data"),
                           tableOutput("")))
    )
  )
)

server <- function(input, output){
  my_data <- reactive({
    req()
    df <- read.csv()
    data <- df[,1]
    return(data)
  })
  
  fitting <- reactive({
    req()
    fit <- list()
    for (i in 1:length()){
      fit[[i]]  <- fitdist(my_data(), )
    }
    f <- fit
    return(f)
  })
  
  output$dataTable <- renderTable({my_data()})
  output$empDen <- renderPlot({
    data <- my_data()
    plotdist(, histo = TRUE, demp = TRUE)})
  output$cfPlot <- renderPlot({descdist(my_data(), discrete=FALSE, boot=500)})
  output$cfSummary <- renderPrint({descdist(my_data(), discrete=FALSE, boot=500)})
  
  output$fitSummary <- renderPrint({
    f <- fitting()
    for (i in 1:length(f)){
      print(summary(f[[i]]))
    }
  })
  
  output$denPlot <- renderPlot({
    f <- fitting()
    #par(mfrow=c(2,2))
    plot.legend <- input$fitInput
    denscomp(f, legendtext = plot.legend)
  })
  
  output$cumluPlot <- renderPlot({
    f <- fitting()
    #par(mfrow=c(2,2))
    plot.legend <- input$fitInput
    cdfcomp (f, legendtext = plot.legend)
  })
  
  output$qqPlot <- renderPlot({
    f <- fitting()
    #par(mfrow=c(2,2))
    plot.legend <- input$fitInput
    qqcomp  (f, legendtext = plot.legend)
  })
  
  output$ppPlot <- renderPlot({
    f <- fitting()
    #par(mfrow=c(2,2))
    plot.legend <- input$fitInput
    ppcomp  (f, legendtext = plot.legend)
  })
  
  output$goodSummary <- renderPrint({
    if (input$goodCheck == TRUE){
      f <- fitting()
      gofstat(f, fitnames = input$fitInput)
    }
  })
  
  output$bootSummary <- renderPrint({
    if (input$uncertCheck == TRUE){
      f <- fitting()
      for (i in 1:length(f)){
        ests <- bootdist(f[[i]], niter = 1e3)
        print(paste0("****",input$fitInput[i],"****"))
        print(summary(ests))
        print(quantile(ests, probs=.05)) 
      }
    }
  })
}

shinyApp(ui=ui, server=server)

