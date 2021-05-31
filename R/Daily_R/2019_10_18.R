## 2019_10_18.R
## 패키지 설치에 있어 알아야 할 것들.
## miniCRAN, match

## 일반적으로 cran 홈페이지에 들어가보면 패키지에 대한 기본적인 정보가 들어가 있다.

## Import.
#  Imports 태그는 필자의 패키지가 Imports 태그에 속한 패키지들이 없으면 작동을 하지 않음을 의미.

## Suggests.
#  Suggests에 속한 패키지들은 있으면 좋지만, 패키지의 주요 기능을 수행하는데에는 이상이 없는 패키지.

## Version.
#  해당 패키지의 버전을 의미

## Built
#  해당 패키지가 제작됐을 때의 R version 환경을 의미

# 예제.
# 현재 설치되어 있는 패키지를 확인해서 package, Import, Depends, Version 컬럼을 추출해보자.
packInfo   <- data.frame(installed.packages())
packInfoEx <- packInfo[,c("Package", "Imports", "Depends", "Version")]

strUdfName <- "packInfo"
strUdfDir  <-  "./"
assign(strUdfName, packInfoEx, pos = 1)
save(list = strUdfName, file = paste0(strUdfDir, "/", strUdfName, ".RData"))


## match function
#  match 함수는 첫 번째 있는 인수가 두 번째 있는 인수의 어디에 위치하는지 알려줌. 


## miniCRAN package
# miniCRAN은 Local 기반의 R Package 설치를 도아주는 Package 
# 일반적인 Package의 Source만 저장하는 것이 아닌 해당 Package의 Dependency까지 자동으로 획득하여 Repo를 구성하며 
# 해당 Repo에 속할 Info파일을 생성 및 관리한다.

install.packages("miniCRAN")

revolution <- c(CRAN="http://cran.revolutionanalytics.com")
pkgs       <- c("foreach")
pkgList <- pkgDep(pkgs, repos=revolution, type="source")