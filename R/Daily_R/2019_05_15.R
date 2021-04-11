# group 변수 별로 결측 처리 
with(df1, ave(v1, ID, FUN = function(x)
  replace(x, is.na(x), x[!is.na(x)][1L])))

# ave function
# 그룹별로 사용자 함수를 적용하는 함수
# ave(x, …, FUN = mean)

# 응용 예제 
# 결측치 처리시, 그룹 평균별로 별로 결측을 대체하고 싶을 때,
# structure function을 이용하여 data.frame을 만들수도 있음
df <- structure(list(ID = c("A", "A", "A", "B", "B", "B", "C", "C","C")
                     , v1 = c(1L, NA, NA, NA, 2L, NA, NA, NA, NA))
                , .Names = c("ID",  "v1"), class = "data.frame", row.names = c(NA, -9L))


df[,"v1"] <- ave(df[,"v1"], df[,grpVar], FUN = function(x){
  impute(x, mean(x, na.rm = T))
})

# replace function
# replace(벡터명, list=변경할 벡터의 인덱스, values=변경할 값)