library(fitdistrplus)
#set the random seed
set.seed(12)

#Generate data based on named distribution
uniform <- runif(100, min=0, max=90)
normal <- rnorm(100, mean=5, sd=1.5)
expon <- rexp(100, rate=1.6)
pois <- rpois(1000, lambda=4)
lognorm <- rlnorm(1000, meanlog=0.6, sdlog=1)

#Plot the randomly generated data 
hist(uniform)
hist(normal)
hist(expon)
hist(pois)
hist(lognorm)

#Write out distribution data
write.csv(pois,"pois_data.csv")
write.csv(lognorm,"task_data.csv")
#Random sampling of generated data
uniSamp <- sample(uniform,20,replace=FALSE)
