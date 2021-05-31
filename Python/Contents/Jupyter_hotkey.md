# Jupyter Notebook 단축키 모음
## Jupyter Lab의 단축키
- <b>ESC</b> 를 눌러 커맨드 모드로 진입하여 ENTER 를 통해 cell 을 수정할 수 있습니다. 아래 커맨드는 커맨드 모드에서 동작합니다. 
- <b>A</b> 는 현재 cell 위에 새로운 cell 을 추가합니다.
- <b>B</b> 는 현재 cell 밑에 새로운 cell 을 추가합니다.
- <b>D + D</b> D를 연속해서 두번 누르면 현재 cell 을 삭제합니다. 
- <b>M</b> 은 Markdown 셀로 변환하며, Y 는 Code 셀로 변환하고  R 은 Raw Cell 로 변환합니다.
- <b>CTRL + B</b> 화면을 더 크게 사용할 수 있습니다. 왼쪽 파일 탐색기가 사라집니다.
- <b>SHIFT + M</b> 두 개의 셀을 한개의 셀로 Merge 합니다.
- <b>CTRL + SHIFT + –</b> 현재 커서 위치를 기준으로 두 개의 셀로 구분합니다. 
- <b>SHIFT+J or SHIFT + DOWN</b> 현재 셀에서 아래쪽 위치로 새로운 셀을 같이 선택합니다. 
- <b>SHIFT + K or SHIFT + UP</b> 현재 셀에서 위쪽 위치로 새로운 셀을 같이 선택합니다. 
- <b>CTRL + /</b> 선택한 코드를 주석처리합니다.
- <b>CTRL+D</b> 한줄 삭제하는 단축키입니다. 
- <b>CTRL+[</b> or <b>CTRL+]</b> 단체 indentation / Tab과 Shift+Tab 으로도 가능하지만, text editor 에서는 Shift+tab 이 안먹혀서 CTRL+[ 을 쓰면 유용합니다. 

## Jupyter Lab 매직 기능 (Magic function)
- 매직 기능은 Ipython kernel 에서 제공  
  Jupyter lab 과 Jupyhter notebook 모두에서 작동합니다.   
  이는 어떤 언어를 선택하든 (예를 들어, Jupyter lab 에서 R을 사용하든 Python 을 사용하든) 동작합니다.
- <b>%matplotlib</b> inline 플롯을 화면 안에서 보여준다.
- <b>%lsmagic</b> 매직 기능에 어떤것들이 있는지 출력해준다. 
- <b>%env</b> 
  - <b>%env</b> 모든 환경변수를 출력한다.
  - <b>%env var</b> 해당 이름의 환경변수를 출력한다.
  - <b>(%env var val) or (%env var=val)</b> 환경변수를 설정한다.
- <b>%run</b> 
  - <b>%run file_name</b> 해당 이름의 .py 파일 또는 .ipynb 파일을 셀 안에서 실행한다. 
- <b>%load</b> 
  - <b>%load source</b> 해당 파일을 셀 안에 로드한다.
  - <b>%who</b> will list all variables that exist in the global scope. It can be used to see what all data_frames or any other variable is there in memory. 
- <b>%who</b> 현재 전역 환경의 모든 변수를 리스트한다. (메모리에 어떤 변수들이 올라와 있나 확인할 수 있다.)
  - <b>%who df</b>: 현재 선언된 dataframe 을 볼 수 있다. 
  - <b>%whos</b> : %who 와 비슷하지만 각 변수들에 대해 상세한 설명을 볼 수 있다. 
  - <b>%time</b> 한 셀이 실행된 시간을 볼 수 있다. 
  - <b>%timeit</b> 10만 번 실행하여 평균 시간을 잰다. 

- <b>%writefile</b> 
  - <b>%writefile file_name</b> 해당 파일의 셀의 아웃풋을 쓴다.
  - <b>%writefile -a file_name</b> 해당 파일의 셀의 아웃풋을 덧붙인다.

## jupyter configuration file (환경설정) 변경하기
- print 문을 쓰지 않고 어떤 변수를 cell 에 입력했을 때, 가장 마지막 줄만 실행해서 결과로 내보내는데, 이것이 불편하다면 아래 문장을 실행하면 됨
~~~python
from IPython.core.interactiveshell import InteractiveShell InteractiveShell.ast_node_interactivity = "all"
~~~

## 참조
- 출처 블로그 : https://3months.tistory.com/392