#Example from: http://www.di.fc.ul.pt/~jpn/r/distributions/fitting.html

library(fitdistrplus)

#Import data and plot
data("groundbeef", package = "fitdistrplus")
my_data <- groundbeef$serving
plot(my_data, pch=20)

#Plot the data as a histogram to visualise the distribution (Note use of ggplot2)
ggplot(data=groundbeef) +
  geom_histogram(mapping=aes(x=serving),bins=10,
                 col="black",
                 fill="grey")

#Plot empirical density and cumulative distribution
plotdist(my_data, histo = TRUE, demp = TRUE)
#Cullen and Frey graph
descdist(my_data, discrete=FALSE, boot=500)
#Fit specific distributions
fit_w  <- fitdist(my_data, "weibull")
fit_g  <- fitdist(my_data, "gamma")
fit_ln <- fitdist(my_data, "lnorm")
summary(fit_ln)

dists <- c("gamma","lnorm","weibull")
fit <- list()
for (i in 1:length(dists)){
  fit[[i]]  <- fitdist(my_data, dists[i])
}

for (i in 1:length(dists)){
  print(summary(fit[[i]]))
}

#Plot the results
par(mfrow=c(2,2))
plot.legend <- c("Weibull", "lognormal", "gamma")
denscomp(list(fit_w, fit_g, fit_ln), legendtext = plot.legend)
cdfcomp (list(fit_w, fit_g, fit_ln), legendtext = plot.legend)
qqcomp  (list(fit_w, fit_g, fit_ln), legendtext = plot.legend)
ppcomp  (list(fit_w, fit_g, fit_ln), legendtext = plot.legend)

par(mfrow=c(2,2))
plot.legend <- dists
denscomp(fit, legendtext = plot.legend)
cdfcomp (fit, legendtext = plot.legend)
qqcomp  (fit, legendtext = plot.legend)
ppcomp  (fit, legendtext = plot.legend)

#Fitting using non-base distributions from the actuar package
library(actuar)

fit_ll <- fitdist(my_data, "llogis", start = list(shape = 1, scale = 500))
fit_P  <- fitdist(my_data, "pareto", start = list(shape = 1, scale = 500))
fit_B  <- fitdist(my_data, "burr",   start = list(shape1 = 0.3, shape2 = 1, rate = 1))
cdfcomp(list(fit_ln, fit_ll, fit_P, fit_B), xlogscale = TRUE, ylogscale = TRUE,
        legendtext = c("lognormal", "loglogistic", "Pareto", "Burr"), lwd=2)

#Goodness of fit statistics
f <- gofstat(fit, fitnames=c("gamma","lnorm","weibull"))
g <- gofstat(list(fit_ln, fit_ll, fit_P, fit_B), fitnames = c("lnorm", "llogis", "Pareto", "Burr"))

#Estimating uncertainty in the parameters
ests <- bootdist(fit_B, niter = 1e3)
summary(ests)
#Plot
plot(ests)
#95% bootstrap confidence interval
quantile(ests, probs=.05)



