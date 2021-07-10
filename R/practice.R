library(mixtools)
data(faithful)

hist(faithful$waiting, 
     main = "Time between Old Faithful eruptions", 
     xlab = "Minutes", 
     ylab = "", 
     cex.main = 1.5, 
     cex.lab = 1.5, 
     cex.axis = 1.4)

wait1 <- normalmixEM(faithful$waiting, lambda = .5, mu = c(55, 80), sigma = 5)
summary(wait1)

plot(wait1, density = T, cex.axis = 1.4, cex.lab = 1.4, cex.main = 1.8,
     main2 = "Time between Old Faithful eruptions", xlab2 = "Minutes")


library(mclust)
mc <- Mclust(iris[,1:4], G = 3)
summary(mc, parameters = TRUE)

library(elasticnet)
set.seed(0)
n_samples <- 30
x         <- runif(n_samples)
x         <- x[order(x)]
y         <- cos(1.5 * pi * x) + rnorm(n_samples) * 0.1
x         <- poly(x, 9, raw=T)
