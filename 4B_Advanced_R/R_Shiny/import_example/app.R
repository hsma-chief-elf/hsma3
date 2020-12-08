library(shiny)

ui <- fluidPage(
  titlePanel("Import data example"),
  
  sidebarLayout(
    sidebarPanel(
      fileInput("upload", "Upload file",
                accept=c("text/csv",
                         "text/comma-separated-values,text/plain",
                         ".csv")
                )
    ),
    mainPanel(
      tableOutput("dataTable")
    )
  )
)

server <- function(input, output){
  my_data <- reactive({
    req(input$upload)
    df <- read.csv(input$upload$datapath)
    data <- df[,1]
    return(data)
  })
  
  output$dataTable <- renderTable({my_data()})
}

shinyApp(ui=ui, server=server)