# 1. file to zip
# 2. 회귀분석 정리

# file을 zip으로 만들어주는 함수
# skill
# 1. list.files를 이용하여 해당 directory의 file list 저장
# 2. zip::zip()를 이용하여 zip 
# 3. 필요하다면 file.remove() 를 이용하여 zip 된 file을 삭제

install.packages("zip")
require(zip)
zip_files <- list.files(path = "./", pattern = ".R")
zip::zip(zipfile = "Zip_files", files = zip_files)

