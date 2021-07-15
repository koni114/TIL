#- 문자열 처리
library(data.table)
df <- data.table::fread('./R/data/access.log',
                        header = F,
                        stringsAsFactors = F)
