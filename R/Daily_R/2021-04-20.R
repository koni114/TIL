#####################
## logging package ##
#####################

#- logging package - open source logging package
#- python의 logging package를 거의 그대로 기능을 구현하려고 한 package

#- 1. 기본 기능 파악하기
#- basic
#- 다음 튜토리얼은 logging package를 사용하기 위한 최소한의 설명을 작성하였음
#- logging library는 python 표준 로깅 라이브러리와 가능한 호환되도록 시도
#- 해당 로깅 라이브러리에 익숙하다면 R의 logging package도 쉽게 사용 가능 할 것임
#- 먼저 logging library를 메모리 상에 로딩하고, basicConfig()를 호출해서 기본 구성을 setting하자

library(logging)
basicConfig()     

#- 중요한 것은 logger와 handler는 environment이므로, ls 와 with를 사용하여 environment 확인 가능
#- defualt로, logger는 basic.stdout이라는 default handler와 INFO라는 level를 가지고 있음
#- 이 두가지는 간단하게 console에 logging하는데 사용될 수 있음

ls(getLogger())
getLogger()[['level']]            #- 현재 root.logger의ㄱdefault loglevel 확인
getLogger()[['handlers']]         #- logger가 가지고 있는 handler list 확인

#- level이 INFO:20 이므로, 이보다 낮은 log level은 console창에 보이지 않음

loginfo('does it work?')          #- 보임
logwarn('my %s is %d', 'name', 5) #- 보임
logdebug('I am a slient child')   #- 보이지 않음

#- addHandler
#- 다른 handler로 추가로 setting 가능한데, 따로 이름을 지정하지 않으면
#- 함수명으로 name이 지정됨. 예를 들어 writeToConsole로 setting
#- 이 handler의 이름을 사용하여 추가하거나, 제거할 수 있음(removeHandler)

addHandler(writeToConsole)
names(getLogger()[['handlers']])  #- writeToConsole 확인
loginfo('test')
logwarn('test')
removeHandler('writeToConsole')   #- handler 삭제 가능
logwarn('test')

#- set level
#- setLevel 함수를 통해 Setting된 level 보다 낮은 단계로 logging 되는 것들은 무시됨
#- 아래와 같이, basic.stdout handler의 log level을 30(WARN)으로 설정하면,
#- 해당 단계보다 낮은 log들은 무시됨
setLevel(30, getHandler('basic.stdout')) #- basic.stdout의 loglevel를 수정하면, 
                                         #- writeToConsole에 대한 내용만 확인 가능
logwarn('test')                           
loginfo('test')                          #- 무시됨
getHandler('basic.stdout')[['level']]

#- herichical logger
#- 앞선 예제들은 하나의 logger(root logger)로만 작업했는데, log 출력 함수들의 입력 파라미터로
#- logger들을 지정할 수 있음. root.logger의 이름은 "" 임
#- 
#- logger는 계층적인 디렉토리 구조와 유사하여, logger에 추가된 handler들이 부모 logger에 전달됨
#- 부모-자식간의 관계는 '.'로 알수 있음

#- logReset후에 다시 살펴보면, heo.jaehun의 계층적 하위 logger들은
#- 부모 logger에 영향을 받아 log가 출력됨을 알 수 있지만 하위 계층의
#- logger가 아닌 경우에는(ex) good ) 출력이 안됨

logReset()
addHandler(writeToConsole, logger = "heo.jaehun")
getLogger("heo.jaehun")[['handlers']] 

loginfo('Ma cos\'è questo amore?', logger='heo.jaehun')
logerror('talking to an unrelated logger', logger='good')

#- logger object
#- getLogger()를 통해서 return된 object는 reference classes임
#- 즉 이 자체로 environment임
#- 다음을 통해 정확히 확인해보자

class(getLogger())          #- logger class
is.environment(getLogger()) #- environment object

#- 즉 RefClass임을 활용하여 다음과 같이 코드를 짜면
#- log출력 함수를 사용할 때마다 logger name을 지정하지 않아도 됨
logReset()
getLogger('heo.jaehun')$addHandler(writeToConsole)
lrc <- getLogger('heo.jaehun.good')
lrc$info('My name is Jaehun heo')
lrc$info('goood!')

logerror('talking to an unrelated logger', logger='rivista.cucina')

#- file에 로깅하기
#- writeToFile이라는 handler를 통해 특정 file에 logging을 할 수 있음.
#- 이때 handler에게 level를 지정할 수 있는데, 이 level보다 높은 것들만 file에 logging 하게 됩니다.
#- 콘솔에는 전부 Logging되도록 하며, file에 writing할 log는 INFO 이상으로 지정해 봅시다
logReset()
basicConfig(level='FINEST')
addHandler(writeToFile, file="~/testing.log", level='INFO')
with(getLogger(), names(handlers))

loginfo('test %d', 1)
logdebug('test %d', 2)
logwarn('test %d', 3)
logfinest('test %d', 4)

#- environment
#- S3 object
#- S4 object
#- 사용 방법

logReset()
basicConfig()
getwd( )
setLevel(30, getHandler('basic.stdout'))
addHandler(rotatingToFile, 
           file="./testing.log", 
           level='DEBUG', 
           maxBytes = 1024 * 1024,
           backupCount = 5,
           formatter = posLogMsgFormat)

loginfo("helloworld")


## the single predefined formatter
posLogMsgFormat <- function(record){
  ## strip leading and trailing whitespace from the final message.
  msg <- trimws(record$msg)
  text <- paste0("[", record$timestamp, "]",
                 "[", record$levelname, "]", record$logger, " >> ", msg)
  return(text)
}


rotatingToFile <- function(msg, handler, ...){
  
  if (length(list(...)) && "dry" %in% names(list(...))){
    return(TRUE)
  }
  
  logFile = with(handler, file)
  
  if (!file.exists(logFile)){
    file.create(logFile)
  }
  
  if (file.info(logFile)[1] >= with(handler, maxBytes)) {
    
    fileList <- vector()
    fileName <- gsub(".log", "", logFile)
    surfixFileName <- ".log"
    
    for(i in 1:with(handler, backupCount)){
      fileList[i] <- paste(fileName, i, surfixFileName, sep = "")
    }
    
    for(i in (with(handler, backupCount):2)){
      if(file.exists(fileList[i-1])){
        if(file.exists(fileList[i])) file.remove(fileList[i])
        file.copy(fileList[i-1], fileList[i])
      }
    }
    
    if(file.exists(fileList[1])){
      file.remove(fileList[1])
    }
    
    file.copy(logFile, fileList[1])
    cat(paste0(msg, "\n"), file = logFile, append = FALSE)    
  }else{
    cat(paste0(msg, "\n"), file = logFile, append = TRUE)
  }
}
