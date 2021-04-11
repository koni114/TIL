## 2019-10-15.R
## 동적 변수를 가지고 rename을 수행하는 방법.
#  match function + colnames function 응용.
library(dplyr)

var1 <- colnames(iris)[c(5,4,3)] 
var2 <- c('c', 'd', 'e')
colnames(iris)[match(var1, colnames(iris), nomatch = 0)] <- var2

