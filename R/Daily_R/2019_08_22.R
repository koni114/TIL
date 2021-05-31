## 2019_08_22
## ggplot2 densitiy plot 생성 방법
## 쌍봉분포 일때의 극소점 찾는 방법 : optimizer, kmeans algorithm 이용

# 1. ggplot2 densitiy plot ----

# density Plot in R
rm(list = ls())

library(datasets)
library(ggplot2)
data(airquality)

# 1. 기본 density plot 생성
# geom_density() function 사용
p8 <-ggplot(airquality, aes(x = Ozone)) +
  geom_density()
p8

# 2. axis label 추가
# scale_x_continuous function 내 name param 사용
# scale_y_continuous function 내 name param 사용
# 줄 바꾸고 싶으면 \n 사용

p8 <- p8 + scale_x_continuous(name = "Mean ozone in parts per billon") +
  scale_y_continuous(name = 'Density')
p8

# 3. 단위 scale 바꾸기
# breaks : 축에서의 간격을 의미. 일반적으로 Data의 최대 최소의 특정 간격을 입력하여 사용
# limits : 축에서의 scale 최대 최소. 
# ** 두개의 값을 잘 입력해야 정상적인 밀도 함수가 나옴.

p8 <- p8 + scale_x_continuous(name   = "Mean ozone in\nparts per billion",
                              breaks = seq(0, 200, 25),
                              limits = c(0, 200))

# 4. title
# 그래프에서의 title은 매우 중요.

p8 <- p8 + ggtitle("Density plot of mean ozone")
p8

# 5. 색깔, 명암 바꾸기
# fill  : 밀도 함수 내 채워지는 색상
# line  : 선 색
# alpha : 명암 ** 주는게 일반적으로 예쁨
fill <- "#4271AE"
line <- "#1F3552"
alpha = 0.6 

p8 <- ggplot(airquality, aes(x = Ozone)) +
  geom_density(fill = fill, colour = line, alpha = 0.6) + 
  scale_x_continuous(name   = "Mean ozone in\nparts per billion",
                     breaks = seq(0, 200, 25),
                     limits = c(0, 200)) +
  scale_y_continuous(name = "Density") + 
  ggtitle("Density plot of mean ozone")


# 6. 바탕색변경 
# theme_bw() : 흰색으로 변경 됨

p8 <- p8 + theme_bw()
p8

# 7. 자신 테마의 그래프 만들기 **
# 정확히는 모르겠지만, panel 등을 이용하여 자신 테마의 그래프를 만들 수 있음.

library(grid)

fill  <- "#4271AE"
lines <- "#1F3552"

p8 <- ggplot(airquality, aes(x = Ozone)) + 
  geom_density(colour = lines, fill = fill, size = 1) +
  scale_x_continuous(name = "Mean ozone in \n parts per billion",
                     breaks = seq(0, 200, 25),
                     limits = c(0, 200)
  ) +
  ggtitle("Density plot of mean ozone") +
  theme_bw() +
  theme(axis.line = element_line(size = 1, colour = "black"),
        panel.grid.major = element_line(colour = "#d3d3d3"),
        panel.grid.minor = element_blank(),
        panel.border     = element_blank(), panel.background = element_blank(),
        plot.title       = element_text(size = 14, family = "Tahoma", face = "bold"),
        text=element_text(family="Tahoma"),
        axis.text.x=element_text(colour="black", size = 9),
        axis.text.y=element_text(colour="black", size = 9))
p8

# 8. 라인 추가하기 **
p8 <- p8 + geom_vline(xintercept = c(75, 135), size = 1, colour = "#FF3721",
                      linetype = "dashed"
)
p8


## 데이터의 분포가 쌍봉 우리 분포일때의 극소점 찾기! **
# 일반적으로 데이터가 two classes 로 분할 하고 싶을때가 있다. (이진 분류 문제와는 다름을 인식하자)

# bimodal distribution을 따르는 data 일때,
mm <- c(418, 527, 540, 553, 554, 558, 613, 630, 634, 636, 645
        , 648, 708, 714, 715, 725, 806, 807, 822, 823, 836, 837
        , 855, 903, 908, 910, 911, 913, 915, 923, 935, 945, 955
        , 957, 958, 1003, 1006, 1015, 1021, 1021, 1022, 1034, 1043
        , 1048, 1051, 1054, 1058, 1100, 1102, 1103, 1117, 1125, 1134
        , 1138, 1145, 1146, 1150, 1152, 1210, 1211, 1213, 1223, 1226, 1334)

mm2 < c(1,2,3,3,3,5,8,12,12,12,12,18)

min_mm2 <- min(mm2, na.rm = T)
max_mm2 <- max(mm2, na.rm = T)

bimodal_df = data.frame(exp1 = mm2)



p8 <- ggplot(bimodal_df, aes(x = exp1)) + 
  geom_density(colour = lines, fill = fill, size = 1) +
  scale_x_continuous(name = "bimodal distribution",
                     breaks = seq(418, 1334, 10),
                     limits = c(418, 1334)
  )
p8

# 이 데이터를 밀도 함수로 변환할 수 있는데,
# 밀도 함수로 변환 했을 때의 x, y 을 이용하자.

d <- density(bimodal_df$exp)

# 결과적으로 극소점을 구하는 것인데, dy/dx = 0을 구하는 것임
# 밀도함수의 x 축 간격은 동일하므로, diff(d$y) 의 절대값이 최소가 되는 점을 찾자.
# 계산하면 다음과 같다.

d$x[which.min(abs(diff(d$y)))]

# 문제는, 극대점도 미분 값이 0이 되므로, 내가 구한 값이 극소값인지, 극대값인지 알기 어렵다.
# 따라서 optimize 함수를 이용해서, 극소점을 찾을 수 있다.

check <- optimize(approxfun(d$x,d$y),interval=c(min_mm2, max_mm2))$minimum
p8    <- p8 + geom_vline(xintercept = check, size = 1, colour = "#FF3721", linetype = "dashed")
p8

# 2. k-means 클러스터링을 이용한 방법

mm <- c(418, 527, 540, 553, 554, 558, 613, 630, 634, 636, 645
        , 648, 708, 714, 715, 725, 806, 807, 822, 823, 836, 837
        , 855, 903, 908, 910, 911, 913, 915, 923, 935, 945, 955
        , 957, 958, 1003, 1006, 1015, 1021, 1021, 1022, 1034, 1043
        , 1048, 1051, 1054, 1058, 1100, 1102, 1103, 1117, 1125, 1134
        , 1138, 1145, 1146, 1150, 1152, 1210, 1211, 1213, 1223, 1226, 1334)

bimodal_df       <- data.frame(exp1 = mm)
d                <- density(bimodal_df$exp1)
km               <- kmeans(bimodal_df$exp1, centers = 2)

bimodal_df$clust <- km$cluster

unique(bimodal_df$clust)

summary1 <- bimodal_df %>% filter(clust == 1) %>% summarise(mean = mean(exp1),
                                                            max  = max(exp1),
                                                            min  = min(exp1)
)

summary2 <- bimodal_df %>% filter(clust == 2)  %>% summarise(mean = mean(exp1),
                                                             max  = max(exp1),
                                                             min  = min(exp1)
)

if(summary1$mean < summary2$mean ){
  check <- mean(summary1$max,  summary2$min)
}else{
  check <- mean(summary1$min,  summary2$max)
}


p8 <- ggplot(bimodal_df, aes(x = exp1)) + 
  geom_density(colour = lines, fill = fill, size = 1) +
  scale_x_continuous(name = "bimodal distribution",
                     breaks = seq(418, 1334, 10),
                     limits = c(418, 1334)
  )

p8 <- p8 + geom_vline(xintercept = check, size = 1, colour = "#FF3721",
                      linetype = "dashed"
)

p8
