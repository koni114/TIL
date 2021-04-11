#' cat 함수를 이용하여 file 저장하기
#' **cat은 엎어쓰기가 default -> append = TRUE로 설정
# 일반적으로 scan() 이용.

cat('John 25', sep = '\n', file = 'test')
cat('Mary 28', sep = '\n', file = 'test', append = TRUE)
cat('Jim 19', sep = '\n', file = 'test', append = TRUE)

#' url을 통해서도 파일을 읽어올 수 있음
#' 구분자에 따른 해당 함수 호출

#' 문자열 처리
#' grep(): 해당 문자열 포함 여부 확인
#' nchar(): 해당 문자열 개수 호출 -> 띄어쓰기 포함
nchar("South Pole") # 10
nchar("SouthPole")  # 9

#' paste(): 두 문자열을 붙이는 함수, sep으로  어떻게 붙일 것인지 설정
paste("a", "b", sep= "-")

#' substr(): start ~ end 까지 문자열을 자르는 함수
#' strsplit(): 구분자를 기준으로 문자열을 split 하는 함수
#' regexpr(), gregexpr(): 문자열 존재 하는 index return

#' 그래프(함수 다루기)
#' 1. 기본적인 plot 그려보기
x <- c(2,5,8,5,7,10,11,3,4,7,12,15)
y <- c(1,2,3,4,5,6,7,8,9,10,11,12)
plot(x, y, main = "PLOT", sub = "Test", xlab ="number", ylab = "value", type="p") # type 에 따라 달라짐

#' plot의 종류
#' boxplot(), pie(), barplot(), hist()
z <-c(3.5, 2.2, 1.5, 4.6, 6.9)

boxplot(x, z) # x, z 두개에 대한 boxplot
pie(x, z)     # x: pie 넓이, z는 pie 그래프에 대한 좌표를 찍음
barplot(x, z) # x: y축, z: x축 bar의 넓이를 의미하는듯. 만약 길이가 맞지 않으면 재사용성 적용
hist(x)       # x data의 도수를 의미. ** barplot과 다름을 인식

#' pairs(): 여러 변수들의 그래프를 한 화면에 출력
#' 이를 통해 데이터의 선형 관계를 파악할 수 있음
a <- data.frame(x,y)
pairs(a)

#' parcoord(): 각 변수들의 값을 연결한 선들의 그래프를 출력
#' parcoord를 통해 각 변수들간의 standardization OR normalization 여부를 파악 가능
#' 그래프를 보고 각 변수들 간의 scale()이 안맞으면 S 또는 n 고려해보아야 한다.
#' But!! 중요한 것은 무작정 S 또는 N을 하면 안된다.
#' 특정 구간 내 데이터 값이 몰려있는데 S,N을 하게 되면 나중에 clustering 등 거리 계산에 문제가 생김 -> 거리 계산 식을 생각해보라
#' 따라서 특정 구간 내에 데이터가 몰려 있다면 z-score를 하거나 outlier 처리를 해서 보는 것이 좋다

#' 기타 및 추가 함수
#' 1. aggregate(): 그룹 별 연산을 위한 함수

aggregate(Sepal.Width ~ Species, iris, mean)

#' 2. melt(): 인자로 데이터를 구분하는 식별자(id), 측정 대상 변수, 측정치를 받아 데이터를 간략하게 표현
#' **궂이 melt를 사용하는 이유: 데이터 분석을 할 때 한 record에 변수 값들을 다 표현해서 봐야하는 경우가 굉장히 많음
#' ggplot2 내에 reshape2 package 설치 필요





