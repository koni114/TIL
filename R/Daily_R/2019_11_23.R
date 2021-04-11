## ggplot2 ,plotly를 이용한 시각화
## plotly와 ggplot을 결합한 boxplot 그리기

library(ggplot2)
library(plotly)



## plotly 를 활용한 box-plot 그리기 ----

# 1. geom_boxplot function 
# boxplot를 그려주는 function. 

# param
# color         ->  box의 '테두리' 색상 지정이 가능. hex code OR 내장 색의 명칭을 입력(ex) c('blue'..))
# outlier.color ->  NULL로 지정하면 outlier.color가 없어짐. 따로 지정도 가능

# 2. scale_fill_manual function
# box 자체에 대한 옵션 지정 가능
# param
# name   : legend에 대한 name 지정(title이 아님!)
# values : hex code를 입력하면 색상이 지정이 가능. 이때 aes에서 color를 지정했다면, 색깔이 바뀌지 않음.
#          fill을 통해 group을 구분했다면, group 개수 만큼 색상을 지정해야함. 

# 3. scale_x_discrete function
# group 별 box에 대한 label을 지정 할 수 있음
# group 개수가 맞지 않으면, 해당 그룹 변수의 level 값을 출력할 것임.(주의)

# 4. labs function
# graph 자체의 x, y, title 지정 가능
# 만약 scale_x_discrete에서 label을 지정했을 시, 해당 label 밑에 X축으로 그게 글씨가 박힘

# 5. theme_light function
# 바탕화면 회색 -> 흰색으로 변경해줌.
# 회색은 칙칙하므로.. 왠만하면 바꿔주자

# 6. theme function
# 그래프 자체의 테마를 변경 해주는 함수수
# param
# legend.position : group에 대한 정보인, legend의 위치 및 출력 여부를 변경 할 수 있음.
#                   ex) "none" 인 경우, legend 출력 안함

expAes1 <- eval( parse(text=paste0("aes(x=", Fvar,", y=",Xvar,", fill=", Fvar,")")))
p <- ggplot(data= test, expAes1) +
  geom_boxplot(width = 0.4, color =  c('#eb7c23','#33802d', '#2cbd1f'), outlier.colour = NULL) +
  scale_fill_manual(name = 'abcd', values = c('#ff8829','#2cbd1f', '#33802d')) +
  scale_x_discrete(labels=c("불량","양호", "최악")) +
  labs(title="", x="",  y="", size=1) +
  theme_light()
# theme(legend.position = "none")

p <- p %>% ggplotly()

## plotly 를 활용한 scatter-plot 그리기 ----

# geom_point function
# 데이터를 점으로 찍어주는 function
# param
# size  : 점의 크기
# alpha : 점의 투명도 조절

# scale_fill_manual function
# 여기서 이 함수를 넣은 이유는, legend의 name을 없애기 위해서! 

# scale_color_manual function
# 점의 색상 지정

# plotly를 적용할 때 aes에 text를 지정하지 않으면, hover text에 보고싶지 않은 값들이 자동으로 들어가 있음.
# 따라서 ggplotly(tooltip = 'text') 를 지정하여 hover text를 조정


test[,'Seq'] <- seq(1:nrow(test))

expAes3 <- eval( parse(text=paste0("aes(x= Seq, y= ",Xvar,",color=",Fvar,", fill=",Fvar, ", text= ", Xvar, ")")))
p <- ggplot(data =test, expAes3) +
  geom_point(size=1, alpha = 1.0) +
  scale_fill_manual(name = '',  values = c('#ff8829','#2cbd1f' ,'#33802d')) +
  scale_color_manual(name = '', values = c("#ff8829", "#2cbd1f",'#33802d')) +
  labs(title="", x="Sequence", y='Value', size=1) +
  theme_light()

p <- p %>% ggplotly(tooltip="text")


## plotly 를 활용한 density-plot 그리기(ggplot 사용 X) ----
# 기본적으로 density function은 y축이 밀도 함수를 위한 계산 값이 필요하므로, density function으로 값을 변환하여 사용. 
# return 객체에 x, y축에 대한 정보가 들어가 있음

SepalL_setosa     <- iris %>% filter(Species == 'setosa') %>% dplyr::select(Sepal.Length) %>%  unlist %>%  unname
SepalL_versicolor <- iris %>% filter(Species == 'versicolor') %>% dplyr::select(Sepal.Length) %>%  unlist %>%  unname

density1 <- density(SepalL_setosa)
density2 <- density(SepalL_versicolor)

# add_trace function(plotly package)
# 해당 함수는 데이터를 추가로 그릴 수 있게 해주는 function
# param
# x :  x축에 들어갈 data
# y :  y축에 들어갈 data
# name : 해당 group의 name
# fill : 채워지는 색깔의 형태를 얘기하는 듯
# fillcolor : 색깔 지정 가능. rgba(a, b, c, d) 형태로 색깔 지정 가능

# layout function(plotly pacakge)
# 그래프 전체의 layout을 setting 할 수 있음
# param
# xaxis : x축 title 지정 및 여러 옵션 존재 
# yaxis : y축 title 지정 및 여러 옵션 존재 

p <- plot_ly(  x = ~density1$x
               , y = ~density1$y
               , type = 'scatter'
               , mode = 'none'
               , name = '불량'
               , fill = 'tozeroy'
               ,fillcolor = 'rgba(255,136,41, 0.8)'
) %>%
  add_trace(x = ~density2$x, y = ~density2$y, name = '양호', fill = 'tozeroy',
            fillcolor = 'rgba(44,189,31, 0.8)') %>%
  layout(xaxis = list(title = 'value'),
         yaxis = list(title = 'Density'))



## plotly 를 활용한 horizontal-bar-plot 그리기(ggplot 사용 X) ----

# plot_ly function
# plotly의 가장 기본이 되는 plot function
# param
# data : 만약 dataFrame 통째로 지정하고 해당 컬럼을 배치하고 싶으면 data param 이용
# x   : x축에 둘 컬럼 setting. 2가지 방식 :: x = ~Sepal.Length,  x = Xvar
# y   : y축에 둘 컬럼 setting. 2가지 방식 :: y = ~Sepal.Length,  y = Yvar
#       ** y축을 정렬하고 싶은 경우,
#       reorder function을 활용!
#       ex) y = ~ reorder(Petal.Length, Sepal.Length)

# hoverinfo : hover text 변경하고 싶을 때 사용 가능. hoverinfo = 'text'
# text      : hover에 출력하고 싶은 text 형식 저장
# type      : plot type 설정
# height    : bar 등의 height 지정
# orientation : bar plot 같은 경우 'h' 입력시, horizontal barplot으로 변경 됨
# marker    : marker param을 이용해서 color를 hex code로 직접 지정할 수 있음

# layout function(plotly package)
# 해당 함수를 통해 x,y title 등을 수정가능
# param
# title : plot의 title 입력
# xaxis     : x축의 title 지정 가능(아래 참고)
# yaxis     : y축의 title 지정 가능(아래 참고)


y <- list(
  title = ""
)

x <- list(
  title = ""
)


p <- plot_ly(   data         =     test
                , x           =  ~ Sepal.Length
                , y           =  ~ reorder(Seq, Sepal.Length)
                , hoverinfo   =   'text'
                , text        = ~ paste0(Species, " : ",Sepal.Length)
                , type        = 'bar'
                , orientation = 'h'
                , marker = list(
                  color = factor(test$Species, labels =  c('#ff8829','#2cbd1f' ,'#33802d'))
                )
)  %>% layout(title = 'Species별 Sepal.Length 크기 정렬', xaxis = x, yaxis = y)



# Tip1. 동적 variable를 이용하여 ggplot 그리기 ----
# eval + parse function을 활용하여 적용

# 예시

test <- iris
Fvar <- 'Species'
Xvar <- 'Sepal.Length'

expAes1 <- eval( parse(text=paste0("aes(x=", Fvar,", y=",Xvar,", fill=", Fvar,")")))
p1      <- ggplot(data= test, expAes1)


# Tip2 동적 plot을 Json data로 변환하기----

pbuild   <- plotly_build(p)
vConents <- pbuild$x %>% toJSON(pretty = TRUE, auto_unbox = TRUE, force = TRUE)