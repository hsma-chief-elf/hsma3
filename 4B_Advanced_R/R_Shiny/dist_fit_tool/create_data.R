library(fitdistrplus)

data("groundbeef", package = "fitdistrplus")
my_data <- groundbeef$serving

write.csv(my_data,'example_data.csv')