"""
intellij 주요 단축키
- shift + shift : 전체 검색.(file, action)
- command + shift + a : action 검색(설정, Refactor 등)
- command + e : 최근 열었던 파일 리스트 보기
- command + [ : 이전/다음 포커스로 이동

break point
- Break Point를 우클릭 하면 조건으로 break을 걸 수 있음
  예를 들어 for, while 등의 반복적인 행위 속에 특정값이 들어올떄만 break 을 하고 싶은 때가 있음

디버깅 버튼(break 가 된 상태에서만 가능)
- resume    : 다음 break point로 이동
- step over : 현재 break 라인 모두 실행 후 바로 다음 라인으로 이동
- step into : 해당 break 라인에서 실행하고 있는 메소드가 있으면 안으로 이동
- force step into
- step out : 해당 라인을 실행 후 이 곳을 호출한 곳으로 거슬러 올라감
- drop frame :  step out과 유사한데 그곳을 호출한 곳까지 가게됨
- run to cursor : 커서가 있는 라인에서 break이 잡히게 됨 break을 안걸고 단발성으로 사용

디버깅 시작하기
- script 화면에서 우클릭하여 debug 'script.py' 클릭
"""

