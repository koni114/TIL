data(nutrient,package = "flexclust")
rownames(nutrient) = tolower(rownames(nutrient))
nutrient.scaled    = scale(nutrient)
d                  = dist(nutrient.scaled)
fit.average        = hclust(d, method="average")
plot(fit.average,hang=-1,cex=.8,main="Average Linkage Clustering")
plot(fit.average)


trainIdx <- caret::createDataPartition(iris[,c(5)], p=0.8, list=F)
train <- iris[trainIdx,  ]
test  <- iris[-trainIdx, ]

fit.km <- kmeans(train[-c(5)], 3, nstart = 50)
fit.km$cluster
fit.km$size
fit.km$centers

predict(fit.km, test)

randIndex(ct.km)
