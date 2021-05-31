#####################################
# dataFrame 내 수치형 변수 return
# Author  : 허재훈
# version : 1.0
# date    : 2019.04.26
#####################################
# CHANGE LOG
#####################################

#' @description 
#' dataFrame 내 수치형 변수 return
#' 
#' @param dataset, 필수, DataFrame

colnames.numeric  <- function(dataset, ...){
  variables <- names(dataset)
  variables[sapply(variables, function(.x) is.numeric(dataset[,.x]))]
  variables <- setdiff(variables, names.time(dataset)) # 날짜형 변수는 제외
  variables
}

#####################################
# dataFrame 내 날짜형 변수 return
# Author  : 허재훈
# version : 1.0
# date    : 2019.04.26
#####################################
# CHANGE LOG
#####################################

#' @description 
#' dataFrame 내 수치형 변수 return
#' 
#' @param dataset, 필수, DataFrame
#' @param onlytime, 필수, T : POSIXct class 만 가지고 오는 경우, F : 전부
#' 
colnames.time <- function(dataset, onlytime = F){
  variables <- base::names(dataset)
  if(onlyTime){
    time_variables <- variables[sapply(variables, function(.x) inherits(dataset[,.x], "POSIXct"))]
  }else{
    # as.POSIXct 변환 가능한 변수도 포함
    # 100개 data 추출 -> na 제거 -> as.poSIXct 적용 후 변환 불가하면 NA, 아니면 변환되므로, all(is.na())를 이용해서 적용
    time_variables <- variables[sapply(variables, function(.x) tryCatch(!all(is.na(as.POSIXct(na.omit(head(dataset[, .x], 100)))))))]
  }
  time_variables
}

#####################################
# dataFrame 내 범주형 변수 return
# Author  : 허재훈
# version : 1.0
# date    : 2019.04.26
#####################################
# CHANGE LOG
#####################################

#' @description 
#' dataFrame 내 categorical 변수 return
#' unique 개수가 2 이상 5이하인 수치형 변수. 수치형 변수는 제외
#' 
#' 
#' @param dataset, 필수, DataFrame
#' @param onlytime, 필수, T : POSIXct class 만 가지고 오는 경우, F : 전부
#'

colnames.categorical <- function(dataset, ...){
  unique_num <- apply(dataset, 2, function(x) length(unique(x[!is.na(x)])))
  variables  <- names(unique_num)[unique_num <= 5 & unique_num > 1]
  c(setdiff(names(dataset), names.numeric(dataset)), variables)
  variables
}

#####################################
# rank 함수(NA 처리)
# Author  : 허재훈
# version : 1.0
# date    : 2019.04.26
#####################################
# CHANGE LOG
#####################################

#' @description 
#' rank+ NA 인 경우 로직 추가
#' rank_index 
#' 
#' @param x, vector
#' @param ties.method, 필수, max, min, 
#' @param na.last, boolean,  na -> last 로 볼것인지의 여부
#' 

rank_na <- function(x, ties.method = "max", na.last = T){
  rank.x <- rank(x, ties.method = ties.method)
  na.index <- is.na(x)
  na.len   <- sum(na.index)-1
  if(na.last){
    rank.x[na.index] <- length(x)- na.len
  }else{
    rank.x[na.index] <- NA
  }
  rank.x
}


#####################################
# apply 활용
# Author  : 허재훈
# version : 1.0
# date    : 2019.04.26
#####################################
# CHANGE LOG
#####################################

#' @description 
#' apply vector일 때에 적용
#' data 가 vector 인 경우, 단순 함수만 적용, DF 이면 apply 함수 적용
#' 
#' @param x, vector
#' @param MARGIN, 필수, 1 : 행, 2 : 열
#' @param FUN, 사용자 함수
#' 
apply.adj <- function(X, MARGIN = 2, FUN){
  if(is.null(dim(X))){
    FUN(X)
  }else{
    apply(X, MARGIN, FUN, ...)
  }
}


#####################################
# 후보 변수 선택
# Author  : 허재훈
# version : 1.0
# date    : 2019.04.26
#####################################
# CHANGE LOG
#####################################

#' @description 
#' 함수를 이용하여 후보 변수 선택
#' 알고리즘 -> logistic, lasso, bagging
#' 
#' @param data, dataset
#' @param yvar, 필수, 1 : 행, 2 : 열
#' @param xvars, yvar를 제외한 나머지 변수
#' @param method, logistic, lasso, bagging 중 하나
#' 
rmf.detect.bin <- function(data, yvar, xvars = setdiff(names(data), yvar),
                           method = c('logistic', "lasso", "bagging")){
  
  # 예측변수 missing 여부 확인
  if(missing(yvar)){
    stop("yvar should be specified")
  }
  
  # 예측 변수 unique 여부 확인 
  if(length(unique(na.omit(data[, yvar]))) <= 1){
    stop("Response variable should have two levels.")
  }
  
  # 예측 변수가 독립 변수에 포함되어 있는 경우 stop
  if(yvar %in% xvars){
    stop("yvar can't be include in xvars.")
  }
  
  # 예측 대상 변수 = 설명 변수분석 대상
  if(is.null(xvars) || length(xvars) <= 1){
    stop("xvars is not proper. (The number of xvars should more than two.)")
  }
  
  # match.args를 통해 method 확인
  method <- match.args(c('logistic', "lasso", "bagging"), method, several.ok = TRUE)
  
  # 각 변수 별 Inf 포함 시 Inf -> NA로 변경
  if(any(is.infinite(as.metrix(data[, xvars])))){
    infinite.variables <- NULL
    for(i in 1:length(xvars)){
      x <- data[, xvars[i]]
      if(any(is.infinite(x))){
        x[is.infinite(x)] <- as.numeric(NA)
        data[,xvars[i]] <- x
        infinite.variables <- union(infinite.variables, xvars[i])
      }
    }
    # 해당 변수에 Inf가 포함되어 있는 경우, print
    infinite.variables <- paste0(infinite.variables, collapse = ", ")
    cat(paste0("Inf, -Inf change to NA value", "\n", "( ", infinite.variables, ")\n"))
  }
  
  # 설명 변수 중 결측 비율이 50% 이상일 때
  # is.na() : 
  missing.xvars <- names(which(sapply(xvars, function(.x) mean(is.na(data[,.x])) >= 0.5)))
  
  if(length(missing.xvars) > 0){
    stop(paste0("Following variables have NA values more than fifty percent."
                , "( ", paste0(missing.xvars, collapse = ", "), ")", "\n"))
  }
  
  # 설명 변수들이 모두 같은 값을 가질 때, stop
  unique.xvars <- names(which(sapply(xvars, function(.x) length(unique(na.omit(data[,.x])))  <= 1 )))
  
  if(length(unique.xvars) > 0){
    stop(paste0("Following variables have only one unique values except NA values.",
                "(", paste0(missing.xvars, collapse = ", "), ")", "\n"
    ))
  }
  
  # 예측 변수 factor 전환
  data[, yvar] <- as.factor(data[,yvar])
  
  # 변수 분석 결과 테이블을 만듬
  out <- data.frame(VARIABLE = xvars, stringsAsFactors = F)
  
  # 1. logistic 
  if("logistic" %in% method){
    logistic.result <- data.frame(t(apply.adj(subset(data, select = xvars), 2, function(x){
      logistic.fit <- glm(as.factor(data[,yvar]) ~ x, family = binomial())
      if(is.numeric(x) && nrow(summary(logistic_fit)$coefficients) == 2){
        log.tmp <- summary(logistic.fit)$coefficients["x", c("z value", "Pr(>|z|)")]        
      }else{
        log.tmp <- c(as.numeric(NA), as.numeric(NA))
      }
      log.tmp
    })))
    out$LOGISTIC_ALPHA   <- logistic_result[, 1]
    out$LOGISTIC_P_VALUE <- logistic_result[, 2]
    out$LOGISTIC_SIGN    <- cut(out$LOGISTIC_P_VALUE, breaks  = c(-Inf, 0.01, 0.05, 0.1, 1), label = c("**", "*", ".", ""))
    out$LOGISTIC_RANK    <- rank_na(out$LOGISTIC_P_VALUE)
  }
  
  if("lasso" %in% method){
    # Guide - lasso 는 x가 2개 이상일 떄 사용
    # lasso.result$beta 에는 각 feature에 대한 coefficient 값이 있음.
    # 
    index.na     <- (apply_adj(subset(data, select = xvars), 1, function(x) any(is.na(x)))) # x값이 na인 경우 return
    lasso.result <- glmnet(as.matrix(subset(data, select = xvars)[!index.na,]), as.factor(data[,yvar][!index_na]), alpha = 1, family ='binomial')
    out$lasso_ZEROBETASOME <- apply_adj(lasso_result$beta, 1, FUN = function(x) sum(which(x==0), na.rm = T))
    out$lasso_RANK         <- rank_na(out$lasso_ZEROBETASOME)
    rm(index_na)
  }
  
  if("bagging" %in% method){
    bag.result <- bagging.tree.noprune(paste(yvar, " ~ ", paste(xvars, collapse = " + ")), data)    
    out$BAGGING <- freq.var(bag.result)[xvars, ]$relative.frequency
    out$BAGGING_RANK <- rank_na(-out$BAGGING, na.last = TRUE)
  }
  
  out$RANK_SUM <- rank_na(rowMeans(cbind(out$COR_RANK, out$LOGISTIC_RANK, out$lasso_RANK, out$BAGGING_RANK), na.rm = T), na.last = TRUE)
  
  out <- out[order(out$RANK_SUM), ]
  rownames(out) <- NULL
  
  return(out)
}


#####################################
# bagging Tree
# Author  : 허재훈
# version : 1.0
# date    : 2019.04.26
#####################################
# CHANGE LOG
#####################################

#' @description 
#' 함수를 이용하여 후보 변수 선택
#' 알고리즘 -> logistic, lasso, bagging
#' 
#' @param formula, rpart에 필요한 formula
#' @param x, 필수, Data 
#' @param y_data, 예측 변수
#' @param no.bootstrap, bootstrap 횟수
bagging.tree.noprune <- function(formula, x, y_data=NULL, no.bootstrap = 50){
  
  require(rpart)
  
  fun.args2  <- as.character(match.call())
  no.of.row  <- dim(x)[1]                       # 데이터의 수
  class.var  <- as.character(names(y_data))     # y
  save.trees <- vector(mode='list', no.bootstrap) # bootstrap 수만큼 tree의 결과를 저장할 틀 생성
  for(i in 1:no.bootstrap){
    boot.sample.index <- sample(no.of.row, no.of.row, replace = TRUE)
    save.trees[[i]]   <- rpart(formula, x[boot.sample.index, ])
    gc(reset = TRUE)
  }
  
  attr(save.trees, "class") <- 'bagging'
  attr(save.trees, "Target.Var") <- class.var
  attr(save.trees, "Exp.Var") <- as.character(formula[3])
  attr(save.trees, "no.bootstrap") <- no.bootstrap
  attr(save.trees, "Levels") <- levels(x[, class.var])
  save.trees
}


#####################################
# bagging 결과 값 저장
# Author  : 허재훈
# version : 1.0
# date    : 2019.04.26
#####################################
# CHANGE LOG
#####################################

#' @description 
#' bagging 결과 값 저장
#' 알고리즘 -> logistic, lasso, bagging
#' 
#' @param bag.tree, bag.tree 객체 -> bagging.tree.noprune return 값
freq.var <- function(bag.tree)
{
  if(class(bag.tree) != "bagging") stop("The class of object is NOT Bagging")
  len.obj <- attributes(bag.tree)$no.bootstrap
  var.used <- c()
  var.used   <- as.character(unique(bag.tree[[1]]$frame$var[!(bag.tree[[1]]$frame$var == "<leaf>")]))
  for(m in 2:len.obj)
  {
    var.used <- c(var.used, as.character(unique(bag.tree[[m]]$frame$var[!(bag.tree[[m]]$frame$var == "<leaf>")])))
  }
  no.var.used <- table(var.used)        # 변수 별 빈도수
  no.var.mat  <- as.matrix(no.var.used) # 변수별 빈도수 matrix 형태로 변경
  no.var  <- rev(sort(no.var.mat[,1]))  # 변수별 빈도 수 높은 순으로 정렬
  no.var2 <- round(no.var/len.obj, 2)   # 빈도수가 높은 순으로 정렬
  var.mat <- as.matrix(no.var)          # 빈도 수 matrix 형태로 변경
  var.mat2 <- cbind(no.var, no.var2)    # 비율(빈도수/bootstrap 횟수) matrix 형태로 변경
  dimnames(var.mat2) <- list(c(dimnames(var.mat)[[1]]), c("frequency", "relative frequency")) # 빈도수와 비율을 하나의 데이터로 통합
  foo.final <- data.frame(var.mat2)
  attr(foo.final, "no.bootstrap") <- len.obj
  foo.final
}

# setdiff(x,y): 차집합 함수, x와 y의 차집합을 구함 
# match.arg : args 를 choices 내 값과 매치하는 함수
# gc: garbage collection, 사용자가 실행 안해줘도 자동 실행

