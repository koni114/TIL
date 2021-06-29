## python algorithm tips
- `sys.stdin.readline()`은 맨 끝의 개행 문자를 반환함  
  따라서 print 함수 내에 그대로 넣으면 개행문자를 출력한 다음 한번 더 개행됨
- FIFO, FILO 등을 수행한다 싶으면 stack을 응용할 수 있음
- 입력의 범위가 주어질 때, 최대, 최소 값은 반드시 테스트해보기
- `while` 문 수행시, 첫 줄에 먼저 check 하고 본문을 수행하자  
  마지막에 check 로직을 넣으면, 예외 잡기가 어려울 수 있음
- 최소, 최대, 0, 1은 반드시 체크 해야 함
- 반올림: `round`, 버림: `int`, 올림: `ceil`


### python 알고리즘 시간 복잡도
- 리스트 중간에 끼워넣거나 빼는 것은 O(N)
- 퀵소트를 직접 구현하면 거의 O(N^2)이 될 확률이 높음. 왠만하면 내장 정렬 함수를 사용하자
- 격자에서 탐색시, 범위 체크
- DP를 Top -> Down 방식으로 할 때는 memorization 필수
- <b>BFS 수행시, queue에서 뺀 다음 확인이 아닌, 큐에서 빼기 전에 방문 체크를 해야 함</b>
- `list.pop`, `list.index`, `list.insert`, `x in list`, `list[:-1]` 전부 O(N)
- list를 queue, deque으로 사용하면 안됨. 반드시 collections.deque를 써야 함

