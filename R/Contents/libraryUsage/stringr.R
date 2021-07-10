#- stringr.
library(stringr)

#- str_c: 문자열 결합
str_c('a', 'b','c', sep = '+')

#- str_length : 문자의 개수
str_length(c('abcd', 'abc'))

#- ** str_extract: 부분 문자열 추출
hw <- "Hadley Wickham"

str_extract(hw, 'Hadley')
