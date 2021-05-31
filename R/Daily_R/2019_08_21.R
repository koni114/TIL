##  2019_08_21
# dplyr package : _all, _at,  _if, vars, funs
# dplyr package : do function 만약 그룹 별로 각각 특정 연산을 함수로 적용하고 싶을 때, 

#' dplyr 부가 기능
#' 동일한 함수를 여러 열에 동일하게 적용해야 한다고 생각해보자.
#' 여러 열은 전부일수도 있고, 특정 조건을 만족하는 열일 수도 있음.

#' _all, _at, _if, vars(), funs() 알아보기.

#' 일반적으로 파생변수를 만들려면, mutate 함수를 이용하여 만들 수 있다.

library(dplyr)
mtcars %>% mutate(exp(qsec)) %>% head

#' 1. _all
#' 만약 모든 열에 대해 지수 함수 exp를 적용해야 한다면 어떻게 해야 할까?
#' _all 이 붙은 함수를 사용하면, 수월하게 사용이 가능하다.
#' 하지만 조심해야 할 점은, 기존의 열이 보존되지 않는다는 점을 조심하자.

mtcars %>% mutate_all(exp) %>%  head(n=3)

#' 2. _at
#' 함수가 적용할 열의 이름이 변수에 저장되어 있는 경우 쓸 수 있음.
coln <- c('cyl', 'disp', 'drat', 'carb')
mtcars %>% mutate_at(coln, exp) %>%  head(n = 3)

#' select 함수 내에서는 따옴표를 사용하지 않고 보통 컬럼을 선택하거나,
#' starts_with, ends_with와 같은 함수를 쓸 수도 있는데, 만약 이러한 방식을 이용하여 _at 안에서 사용하고 싶을 때,
#' vars를 사용한다.

mtcars %>% mutate_at(vars(starts_with('c'), starts_with('d')), exp) %>% head(n=3)

#' 3. _if
#' 특정한 조건을 만족하는 열만을 선택해서 함수를 적용.
#' 만약 열의 총 합이 100 미만인 열에 대해서만 지수 함수 exp를 적용하고 싶다면, 다음과 같이 쓸 수 있음.

mtcars %>% mutate_if(function(x) sum(x) < 100, exp) %>% head(n = 3)

#' 만약, 새로운 열을 생성하면서 함수가 적용되지 않은 열은 제거하고 싶다면,
#' transmute 함수를 사용.

mtcars %>% transmute(expCarb = exp(carb)) %>% head(n=3) 
mtcars %>% transmute_if(function(x) sum(x)<100, exp) %>% head(n=3) 

# 특정 조건에 해당하는 컬럼을 변형하여 return 할수도 있다.!! (매우 편리..)
mtcars %>% mutate_if(funs(sum(.) >= 100), funs(paste(.,"+",sep=""))) %>% head(n=3)

# dplyr::do 
# 만약 그룹 별로 각각 특정 연산을 적용하고 싶을 때, dplyr::do function 사용 가능!
# do 함수는 항상 dataframe을 return
library(dplyr)
by_cyl <- dplyr::group_by(mtcars, cyl)
do(by_cyl, head(., 2))

# group_by 별로 lm 모델을 만들고 varName, coef 결과를 확인하고 싶을 때,

models <- by_cyl %>% do(mod = lm(mpg ~ disp, data = .))
summarise(models, rsq = summary(mod)$r.squared)
models %>% do(data.frame(
  var  = names(coef(.$mod)) 
  , coef = coef(.$mod))
)

# group_by 별로 linear, quad lm model을 만들고,  p-value를 비교하고 싶을 때,
# do 함수 내부적으로 2개의 결과 변수를 만들고, 이를 각각 호출할 수 있음.

models <- by_cyl %>% do(
  mod_linear = lm(mpg ~ disp, data = .),
  mod_quad   = lm(mpg ~ poly(disp, 2), data = .)
)

compare <- models %>% do(aov = anova(.$mod_linear, .$mod_quad))



