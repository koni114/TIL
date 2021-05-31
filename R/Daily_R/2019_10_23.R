# 2019_10_23.R
# writen  : 허재훈
# created : 2019.10.23
# miniCRAN, 인터넷이 안될 때, local repo를 이용하여 tar.gz download 받고, 이를 설치하는 방법 guide


# miniCRAN 사용해보기

#  miniCRAN는 Local 기반의 R Package 설치를 도와주는 Package.
# 핵심은, 일반적인 Package의 Source만 저장하는 것이 아닌 해당 Package의 Dependency까지 자동으로 획득하여 Repo를 구성하며,
# 해당 Repo에 속할 Info파일을 생성 및 관리.
# ** 특히 CRAN, CRAN Mirror사이트 외에도 Bioconductor,R-forge, Repository의 정보를 종합 및 취합할 수 있는 장점이 있음.

# 1. Install 하기
# 최초 Install은 Internet 환경에서 R을 실행 해야한다.
# 해당 실행은 기본 Repo에서 실행하게 됨 -> 여기서 말하는 repository는 우리가 패키지를 다운 받을 "패키지 저장소"를 말한다.
# 실제로 repository라고 하는 용어는 패키지, 라이브러리 소스가 저장되어 있는 경로를 통칭한다.

# 기본적으로 CRAN -> "http://cran.rstudio.com/" 으로 되어 있을 것이다.

install.packages("miniCRAN")  # miniCRAN 패키지 설치
library(miniCRAN)
getOption("repos")            # 기본 repo 확인 

# 2. dependency package List 뽑아오기
# Vector 형태로 이루어진 문자형의 Package를 통해 pkgDep 함수를 사용하면 Return 값으로 해당 Dependency의 Tree를 문자형의 나열된 Vector로 반환한다.

# 예를 들어, dplyr의 종속된 dependency package를 가져와보자.
pkgs    <- c("dplyr")
pkgList <-pkgDep(pkgs, type = "source")

pkgList # dplyr package에 종속된 package 목록을 확인할 수 있다.

# 3. Repository 생성
# makeRepo function을 통해 pth 경로에 Source를 포함한 Repository를 생성한다.

dir.create(pth <- file.path(getwd(), "miniCRAN"))
dirPkgList <- makeRepo(pkgList, path = pth, type = "source", Rversion = "3.6")

# 4. 참조 : graph로 dependency 정보를 확인
# makeDepGraph function을 이용해서 dependency 정보를 눈으로 확인할 수 있음. 

dg <- makeDepGraph(pkgList[1], enhances = TRUE, availPkgs = cranJuly2014)
set.seed(1)
plot(dg, legendPosition = c(-1, -1), vertex.size = 10, cex = 0.7)

# 5. local repository를 이용하여 package 설치해보기 -> tar.gz file을 설치하려면, Rtools가 선행적으로 깔려있어야 함.

uninstallPkg <- c()
pkgFullDirName <- dirPkgList[1]
# pkgFullDirName <- "C:/rTest/miniCRAN/src/contrib/magrittr_1.5.tar.gz"

# pkgList <- apply(data.frame(dirPkgList), 1, function(x){
#   tmpVec  <- strsplit(x, "/")[[1]]
#   pkgName <- strsplit(tmpVec[length(tmpVec)], "_")[[1]][1]
#   pkgName
# })


######################################
# InstallPack
# local package install시 dependency 고려한 install function
# ** uninstallPkg <- c(), pkgList vector가 선행되어 있어야함.
# pkgList -> packageName list
# Author     : 허재훈
# version    : 1.3
# location   : local R
#####################################
# CHANGE LOG
# 1.0   : initial version
#####################################
#' @param pkgFullDirName, directory + PackageName + tar.gz,
#' @examples
#' InstallPack(pkgFullDirName = 'C:/rTest/miniCRAN/src/contrib/magrittr_1.5.tar.gz'")
InstallPack <- function(pkgFullDirName){
  
  print(paste0("****** ", pkgFullDirName , " start !!"))
  
  # 파싱을 통해 packageName만 추출.
  tmpVec  <- strsplit(pkgFullDirName, "/")[[1]]
  pkgName <- strsplit(tmpVec[length(tmpVec)], "_")[[1]][1]
  
  # 이미 있는 package면, return
  if(any(installed.packages()[,c("Package")] %in% pkgName)){
    print(paste0("이미 있는 package :", pkgName))
    return(NULL)
  }
  
  # 해당 package의 dependency package가 있는지 확인 
  dependsPkg <- tools::package_dependencies(pkgName)[[1]]
  print(paste0("depends pack : ", dependsPkg))
  
  # dependency package가 없으면 input param의 package만 설치하고 종료.
  if(length(dependsPkg) < 1){
    
    # install.packages function을 통해 package install. 이 때 error 발생시, 전역변수인 uninstallPkg vector에 append
    tryCatch({
      install.packages(pkgFullDirName, repos = NULL, type = "source")
      print(paste0("####### ", pkgName, " is installed ##########"))
    }, error = function(err) {
      uninstallPkg <- c(uninstallPkg, pkgName)
    })
    return(NULL)
    
    # dependency package가 있으면, 재귀적 호출을 통해, 다시 InstallPack function의 입력 변수로 setting
  }else{
    
    # dependency package vector를 for문을 통해 재귀적 호출 진행.
    for(tmp in dependsPkg){
      print(paste0("tmp : ", tmp))
      
      # 해당 dependency package의 dir + packageName + tar.gz 로 paste 후 함수에 다시 입력. 
      if(any(pkgList %in% tmp)){
        InstallPack(dirPkgList[pkgList %in% tmp])
      }
    }
    
    # install.packages function을 통해 package install. 이 때 error 발생시, 전역변수인 uninstallPkg vector에 append
    tryCatch({
      install.packages(pkgFullDirName, repos = NULL, type = "source")
      print(paste0("## ", pkgName, " is installed"))
    }, error = function(err) {
      uninstallPkg <- c(uninstallPkg, pkgName)
    })
    return(NULL)
  }
}
