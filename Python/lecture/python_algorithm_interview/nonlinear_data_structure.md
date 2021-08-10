#  비선형 자료구조
- 데이터 요소가 순차적(Sequential)으로 또는 선형으로 배열되지 않는 자료구조를 비선형(Non-linear) 자료구조라고 함
- 비선형 자료구조는 선형과 달리 멀티 레벨로 구성됨
- 트리를 떠올리면 이해하기가 쉬운데, 탐색이 복잡하고 선형에 비해 구현하기도 복잡하지만, 메모리를 좀 더 효율적으로 활용할 수 있다는 장점이 있음
- 대표적으로는 그래프를 예로 들 수 있으며, 그래프의 범주에 포함되는 트리 또한 비선형 자료구조임

## chapter12 그래프
- 그래프 이론에서 그래프란 객체의 일부 쌍들이 '연관되어' 있는 객체 집합 구조를 말함

### 오일러 경로
- 모든 간선을 한 번씩 방문하는 유한 그래프를 오일러 경로라고 함
- 한붓 그리기를 생각하면 쉬움
- 증명에 따르면 모든 정점이 짝수개의 차수를 갖지 않으면 오일러 경로가 아니라고 함

### 해밀턴 경로
- 각 정점을 한 번씩 방문하는 무항, 유항 그래프 경로를 말함
- 오일러 경로는 edge를 기준으로 하지만, 해밀턴 경로는 node를 기준으로 함
- 해밀턴 경로를 찾는 문제는 최적 알고리즘이 없는 대표적인 NP-complete 문제임
- 원래의 출발점으로 돌아오는 경로는 특별히 해밀턴 순환(Hamiltonian Cycle)이라 하는데, 이중에서도 특히 최단 거리를 찾는 문제는 알고리즘 분야에서는 외판원 문제(Traveling Salesman Problem)로도 유명함
- 외판원 문제란 각 도시를 방문하고 돌아오는 가장 짧은 경로를 찾는 문제로 유명

### NP 복잡도
- NP는 비결정론적 튜링 기계로 다항 시간 안에 풀 수 있는 판정 문제의 집합으로, NP는 비결정론적 다항시간(Non-deterministic Polynomial time)의 약자
- NP에 속하는 문제는 결정론적 튜링 기계로 다항 시간에 검증이 가능하고, 그 역도 성립 
- 결정론적 튜링 기계로 다항 시간 안에 풀 수 있는 문제는 비결정론적 튜링 기계로도 다항 시간 안에 풀 수 있으므로, P 집합은 NP 집합의 부분집합

### 그래프 순회
- 그래프의 각 정점을 방문하는 그래프 순회는 크게 DFS, BFS가 있음
- 대부분 BFS에 비해 DFS가 더 널리알려져 있으며, 그래프 탐색은 보통 DFS로 많이 짬
- DFS는 주로 stack으로 구현하거나 재귀로 구현하며, 이후에 살펴볼 백트래킹을 통해 뛰어난 효용을 보임
- BFS는 주로 queue로 많이 구현하며, 그래프의 최단 경로를 구하는 문제 등에 사용됨
- 그래프를 표현하는 방법으로 크게 인접 행렬(Adjacency Matrix)와 인접 리스트(Adjacency List)의 두가지 방법이 있음
- 인접 리스트는 출발 노드를 key로, 도착 노드를 value로 표현 가능

#### DFS(깊이 우선 탐색)
- 재귀 구조로 표현한 코드는 다음과 같음
~~~python
graph = {
    1: [2, 3, 4],
    2: [5],
    3: [5],
    4: [],
    5: [6, 7],
    6: [],
    7: [3],
}

def recursive_dfs(v, discovered=[]):
    discovered.append(v)
    for w in graph[v]:
        if not w in discovered:
            recursive_dfs(w, discovered)
    return discovered


recursive_dfs(1, [])
#- [1, 2, 5, 6, 7, 3, 4]
~~~
- stack을 이용한 반복 결과로 DFS를 구현하면 다음과 같음
~~~python
def iterative_dfs(start_v):
    discovered = []
    stack = [start_v]
    while stack:
        v = stack.pop()
        if v not in discovered:
            discovered.append(v)
            for w in graph[v]:
                stack.append(w)
    return discovered

iterative_dfs(1)
#- [1, 4, 3, 5, 7, 6, 2]
~~~
- 재귀는 조금더 코드가 깔끔하고, stack은 성능이 더 빠르다
- 두개의 코드에서 방문 순서가 다른데, 재귀식 DFS는 사전식 순서로 방문한 데 반해, stack DFS는 역순으로 방문함

#### BFS(너비 우선 탐색)
- BFS는 DFS보다 쓰임새는 적지만, 최단 경로를 찾는 다익스트라 알고리즘 등에 매우 유용하게 쓰임
- BFS를 queue를 사용해 반복 구조로 구현해보자
~~~python
def iterative_bfs(start_v):
    discovered = [start_v]
    queue = [start_v]
    while queue:
        v = queue.pop()
        for w in graph[v]:
            if w not in discovered:
                discovered.append(w)
                queue.append(w)
    return discovered
~~~
- BFS는 재귀로는 동작하지 않음. 큐를 이용하는 반복 구현만 가능

### 백트래킹
- 백트래킹(BackTracking)은 해결책에 대한 후보를 구축해 나가다가 가능성이 없다고 판단되는 즉시 후보를 포기해 정답을 찾아가는 범용적인 알고리즘으로 제약 충족 문제(Contraint Satisfaction Problems)에 유용
- DFS를 이야기하다 보면 항상 백트래킹이라는 단어가 함께 나옴
- 백트래킹은 DFS와 같은 방식으로 탐색하는 모든 경우를 말함
- 백트래킹은 주로 재귀로 구현하며 알고리즘마다 DFS 변형이 일어나긴 하지만 기본적으로 모두 DFS의 범주에 속함
- 트리의 가지치기 같은 경우, 불필요한 부분을 일찍 포기하는 백트래킹을 사용한다면 성능을 조금 향상시킬 수 있음

### 제약 충족 문제(Contraint Satisfaction Problems)
- 백트래킹은 제약 충족 문제를 풀이하는 데 필수적인 알고리즘임. 앞서 살펴본 가지치기를 통해 제약 충족 문제를 최적화 하기 때문
- 스도쿠같은 문제도 백트래킹을 하면서 가지치기를 통해 최적화하는 형태로 풀이할 수 있음
- 십자말 풀이, 8퀸 문제, 4색 문제 같은 퍼즐 문제와 배낭 문제, 문자열 파싱, 조합 최적화 문제 등이 모두 제약 충족 문제에 속함

### 섬의 개수 문제
- 1을 육지로, 0을 물로 가정한 2D 그리드 맵이 주어졌을 때, 섬의 개수를 계산해라
~~~python
from typing import List
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        H, W = len(grid), len(grid[0])
        island_num = 0
        ax = [1, -1, 0, 0]
        ay = [0, 0, 1, -1]
        def dfs(i, j):
            stack = [(i, j)]
            while stack:
                x, y = stack.pop()
                grid[x][y] = 0
                for i in range(4):
                    cx, cy = x + ax[i], y + ay[i]
                    if 0 <= cx <= H-1 and 0 <= cy <= W-1 and grid[cx][cy] == "1":
                        stack.append((cx, cy))

        for i in range(H):
            for j in range(W):
                if grid[i][j] == "1":
                    dfs(i, j)
                    island_num += 1

        return island_num
~~~

### 중첩 함수(Nested function)
- 함수 내에 위치한 또 다른 함수로, 바깥에 위치한 함수들과 달리 부모 함수의 변수를 자유롭게 읽을 수 있다는 장점이 있음
- 실무에서는 자주 쓰이는 편은 아니지만 단일 함수로 해결해야 하는 경우가 잦은 코딩 테스트에서는 매우 자주 쓰이는 기능 중 하나
- 중첩 함수가 부모 함수의 변수를 공유하는 예제는 다음과 같음
~~~python
def outer_function(t: str):
    text: str = t

    def inner_function():
        print(text)

    inner_function()

outer_function('Hello!')
~~~
- 가변 객체인 경우, `append`, `pop`등 여러 가지 연산으로 조작도 가능함
- 그러나 재할당(=)이 일어날 경우 참조 ID가 변경되어 별도의 로컬 변수로 선언되므로 주의가 필요

### itertools 모듈 사용
- 파이썬에서는 itertools라는 모듈이 있음. itertools 모듈은 생성에 최적화된 효율적인 기능들을 제공하므로, 실무에서는 알고리즘으로 직접 구현하기보다는 가능하다면 itertools 모듈을 사용하는 편이 나음
- 이미 잘 구현된 라이브러리이며 직접 구현함에 따른 버그 발생이 낮고, 무엇보다도 효율적으로 설계된 C 라이브러리라 속도에도 이점이 있음
- 온라인 인터뷰시 직접 구현하라는 얘기가 있을 수 있지만, 별도의 제약사항이 없는 이상 안쓸 이유가 없음
- 주석으로 "구현의 효율성, 성능을 위해 사용" 등의 설명을 달아둔다면 됨
~~~python
def permute(self, nums: List[int]):
    return list(itertools.permutations(nums))
~~~

### 객체 복사
- 복잡한 리스트의 경우는 `[:]`로 해결되지 않음. `deepcopy()`를 사용해야 함

### 백트래킹(DFS)을 활용한 순열과 조합 
~~~python
class Solution:
    #- 순열
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = []

        def dfs(curr, rest):
            if not rest:
                result.append(curr[:])
                return

            for e in rest:
                curr.append(e)
                tmp = rest[:]
                tmp.remove(e)
                dfs(curr, tmp)
                curr.pop(e)

        dfs([], nums)
        return result

    #- 조합
    def combine(self, n: int, k: int) -> List[List[int]]:
        def dfs(index, curr_list):
            if len(curr_list) == k:
                results.append(curr_list[:])
                return

            for i in range(index, n+1):
                curr_list.append(i)
                dfs(i + 1, curr_list)
                curr_list.pop()

        results = []
        dfs(1, [])

        return results
~~~