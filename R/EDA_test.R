library(ggplot2)
#- 1. iris 데이터를 활용하여 scatter plot을 그려보세요
#- 2. 위에서 그린 scatter plot에서 추세선을 그려보세요
#- 3. 산점도에서 x => Sepal.Length, y = Sepal.Width를 그리는데, Sepal.Length 값이 5보다 크면 빨강, 5보다 작으면 검은색으로 나타내보자
#- 4. 2번에서 그린 scatter plot에서 추세선에 대한 다음과 같은 text를 입력해 보세요. --> y = 6.452x-18.142 
#- 5. ggplot 객체를 .png로 저장하려면 어떻게 해야하는가? 
#- 6. 2번 그래프에서, Sepal.Length (5, 7),  Sepal.Width(2.5, 3.5) 범위로 사각형을 그려보아라
#- 7. economics data에서 x은 시계열이고, y는 unemploy 로 하여 값을 알아볼 수 있는 그래프를 그리세요
#- 8. mpg data에서 awy의 개수를 count하는 area plot를 그려보세요.
#- 9. Species 별 Sepal.Legnth의 밀도함수를 그려보세요! 이 때 색깔은 빨강, 파랑, 초록입니다.
#- 10. titanic data에서 Pclass 빈도수를 histogram으로 나타내세요
#- 11. 막대 그래프를 통해 Survived 별 Pclass 개수를 확인하세요
#- 12. 그래프의 제목, 부제목, x, y명 변경 방법은 무엇인가? 
#- 13. iris


########
# 정답 #
########

#- 1.
library(ggplot2)
p <- ggplot(data = iris,
            mapping = aes(x = Sepal.Length, y = Sepal.Width)
            ) + geom_point(colour = c('blue', 'green', 'red')[iris$Species])
print(p)

#- 2
p + ggplot2::stat_smooth(method = 'lm', se=F, color='black')

#- 3
p <- ggplot(data = iris,
            mapping = aes(x = Sepal.Length, y = Sepal.Width)
            ) + geom_point(aes(colour = ifelse(Sepal.Length >= 5.0, 'a', 'b')
                           )) + scale_color_manual(values = c('red', 'black'),
                                                   name = NULL,
                                                   labels = c('more than 5', 'less than 5')
                                                  )

#- 4
p <- ggplot(data = iris,
            mapping = aes(x = Sepal.Length, y = Sepal.Width)
            ) + geom_point(colour = c('red', 'green', 'blue')[iris$Species]
                           ) + stat_smooth(method='lm', se = F, color='black'
                                           ) + geom_text(x =5.5, y = 3.2, label = ' y = 6.452x-18.142 ')

#-5 x
ggsave('test.png', plot = p)

#-6
p2 <- p + geom_rect(aes(xmax = 7,
                    xmin = 5,
                    ymax = 3.5,
                    ymin = 2.5))
print(p2)

#-7
p <- ggplot(data = economics,
            mapping = aes(x = date, y = unemploy)
            ) + geom_area(alpha = 0.5)
print(p)

#- 8
g <- ggplot(mpg,
            aes(hwy)
            ) + geom_area(stat = 'bin')

#- 9
g <- ggplot(data = iris,
            mapping = aes(x = Sepal.Length, fill = Species, color = Species)
            ) + geom_density( alpha = 0.5)
print(g)

#- 10.
colnames(titanic)
g <- ggplot(data = titanic,
            mapping = aes(x = Age, fill=Embarked, color=Embarked)
            ) +  geom_histogram(bins=50, alpha = 0.3)
print(g)

#- 11
colnames(titanic)
str(titanic)
g <- ggplot(data = titanic
            )+ geom_bar(stat='count', aes(x = Survived, fill=as.factor(Pclass))) + scale_fill_manual(values = c('red','blue', 'green'),
              name='hello world', 
              labels=c('1', '2', '3'))
print(g)

#- 12.
p <- ggplot(data = iris,
            mapping = aes(x = Sepal.Length, y = Sepal.Width)
) + geom_point(colour = c('blue', 'green', 'red')[iris$Species])
p + labs(title = 'hello world', x='xname', y='yname')

library(ggplot2)
library(reshape2)
data <- iris
data$seq <- 1:nrow(iris)
dataMelt <- reshape2::melt(data, id.vars = c('seq'), 
               measure.vars = c('Sepal.Length', 'Sepal.Width', 'Petal.Length', 'Petal.Width'))

g <- ggplot(data = dataMelt,
            mapping = aes(x = seq, y = value, color=variable)
            ) + geom_line() + scale_color_manual(
              values = cols,
              name = 'hello',
              labels =  c('Sepal.Length', "Sepal.Width", "Petal.Length", "Petal.Width")
            )
print(g)

