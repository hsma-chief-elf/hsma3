library(shiny)

# Define the page layout type ----
ui <- fluidPage(
  # App title ----
  titlePanel("My first web app"),
  # Sidebar layout with input and output definitions ----
  sidebarLayout(
    # Sidebar panel for inputs ----
    sidebarPanel(
      h3("A sidebar panel"),
      p("In the side bar I can place
        all of my input selection options
        for what I want to happen in the
        main panel")
    ),
    # Main panel for displaying outputs ----
    mainPanel(
      # Outputs to be displayed
      h3("The main panel"),
      p("In the main panel I would place
        all of my outputs which change
        given the inputs in the sidebarPanel")
    )
  )
)
# Define server logic which is how the inputs will be used to produce the outputs ----
server <- function(input, output){}
# Create Shiny app ----
shinyApp(ui=ui, server=server)