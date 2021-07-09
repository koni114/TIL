library(rcompanion)
library(nortest)
data("airquality")
rcompanion::plotNormalHistogram(airquality$Ozone)

nortest::ad.test(airquality$Ozone)
