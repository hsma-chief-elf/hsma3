library(shiny)

# Define the page layout type ----
ui <- fluidPage(
  # App title ----
  titlePanel("Tabsets"),
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
      
      # Output: Tabset w/ plot, summary, and table ----
      tabsetPanel(type = "tabs",
                  tabPanel("Plot", p("Here I could place some plots perhaps")),
                  tabPanel("Summary", p("Here I might have some summary statistics")),
                  tabPanel("Table", p("This might be a table of the raw data"))
      )
      
    )
  )
)

# Define server logic which is how the inputs will be used to produce the outputs ----
server <- function(input, output) {}

# Create Shiny app ----
shinyApp(ui, server)