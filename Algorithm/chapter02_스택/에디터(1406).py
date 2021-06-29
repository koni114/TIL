"""
- 영어 소문자만 입력
- 최대 600,000 글짜까지 입력 가능
- 커서는 문장의 맨 앞, 문장의 맨 뒤, 문장 사이 사이에 위치할 수 있음
- 길이가 L인 문자열이 현재 편집기에 입력되어 있으면, 커서가 위치할 수 있는 곳은 L+1임
- 편집기가 지원하는 명령어
  - L: 커서를 왼쪽으로 한칸 옮김(커서가 맨 앞이면 무시)
  - D: 커서를 오른쪽으로 한칸 옮김(커서가 문장의 맨 뒤면 무시됨)
  - B: 커서 왼쪽에 있는 문자 삭제(커서가 문장의 맨 앞이면 무시됨)
  - P: $라는 문자를 커서 왼쪽에 추가함
- 초기에 편집기에 입력되어 있는 문자열이 주어짐
- 이후 입력한 명령어가 차례로 주어졌을 떄, 명령어 수행
- 명령어가 수행되기 전에 커서는 문장의 맨 뒤 위치
"""
#- front, back이란 stack 두 개 만듬
#- 최초 입력 문자열은 front에 만듬
import sys
from collections import deque
inf = sys.stdin
front = deque(list(inf.readline().strip()))
back = deque()

n = int(inf.readline().strip())
for _ in range(n):
    command = list(inf.readline().strip().split())
    if command[0] == 'L':
        if len(front):
            back.appendleft(front.pop())
    elif command[0] == 'D':
        if len(back):
            front.append(back.popleft())
    elif command[0] == 'B':
        if len(front):
            front.pop()
    else:
        front.append(command[1])

print("".join(front + back))
