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

### 일정 재구성 문제
- [from, to]로 구성된 항공권 목록을 이용해 JFK에서 출발하는 여행 일정 구성하기
- 여러 일정이 있는 경우 사전 어휘 순으로 방문함

### 최단 경로 문제
- 최단 경로 문제는 각 간선의 가중치 합이 최소가 되는 두 정점사이의 경로를 찾는 문제
- 이런 최단 경로 문제는 그래프의 종류와 특성에 따라 각각 최적화된 다양한 최단 경로 알고리즘이 존재함
- 이 중에서 가장 유명한 것은 다익스트라 알고리즘
- 다익스트라 알고리즘은 항상 노드 주변의 최단 경로만을 택하는 대표적인 그리디 알고리즘 중 하나로, 단순할 뿐만 아니라 실행 속도 또한 빠름
- 다익스트라 알고리즘은 노드 주변을 탐색할 때, BFS를 이용하는 대표적인 알고리즘이기도 함
- 하지만 가중치가 음수인 경우에는 처리할 수 없음
- 다익스트라 알고리즘은 임의의 정점을 출발 집합에 더할 때, 그 정점까지의 최단거리는 계산이 끝났다는 확신을 갖고 더함
- 만일 이후에 더 짧은 경로가 존재한다면, 다익스트라 알고리즘의 논리적 기반이 무너짐
- 이때는 모두 값을 더해 양수로 변환하는 방법이 있으며, 이마저도 어렵다면 벨만-포드 알고리즘 같은, 음수 가중치를 계산할 수 있는 다른 알고리즘을 사용해야 함
- BFS + priorityqueue 를 적용할 경우, 시간 복잡도는 O(V+E), 모든 정점이 출발지에서 도달이 가능하다면, O(ElogV)가 됨

### 네트워크 딜레이 타임
- K부터 출발해 모든 노드가 신호를 받을 수 있는 시간을 계산해라. 불가능할 경우 -1을 리턴
- 입력값 (u, v, w)는 각각 출발지, 도착지, 소요 시간으로 구성되며, 전체 노드의 개수는 N으로 입력받음

#### 전체 코드
~~~python
def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        graph = collections.defaultdict(list)
        #- 그래프 인접 리스트 구성
        for u, v, w in times:
            graph[u].append((v, w))

        # 큐 변수: [(소요시간, 정점)]
        Q = [(0, k)]
        dist = collections.defaultdict(int)

        while Q:
            time, node = heapq.heappop(Q)
            if node not in dist:
                dist[node] += time
                for v, w in graph[node]:
                    alt = time + w
                    heapq.heappush(Q, (alt, v))

        #- 모든 노드의 최단 경로 존재 여부 판별
        if len(dist) == n:
            return max(dist.values())
        return -1
~~~

#### 코드 단위별 파악해보기
~~~python
 graph = collections.defaultdict(list)
        #- 그래프 인접 리스트 구성
        for u, v, w in times:
            graph[u].append((v, w))
~~~
- 문제의 입력값 (u, v, w)를 키/값 구조로 조회할 수 있는 그래프 구조(인접 리스트)로 변경
~~~python
 # 큐 변수: [(소요시간, 정점)]
Q = [(0, k)]
dist = collections.defaultdict(int)
~~~
- 큐 변수 Q는 '(소요시간, 정점)' 구조로 구성함. 즉 시작점에서 '정점'까지의 소요 시간을 담아 둘 것임
~~~python
while Q:
    time, node = heapq.heappop(Q)
    if node not in dist:
        dist[node] += time
        for v, w in graph[node]:
            alt = time + w
            heapq.heappush(Q, (alt, v))
~~~
- 큐 순회를 시작하자마자 최솟값을 추출한 후, dist에 node 포함 여부부터 확인
- 이미 dist에 키가 존재한다면 그 값은 버리게 되는 것이 핵심

### K 경유지 내 가장 저렴한 항공권
- 다익스트라 알고리즘과 유사하나 K개의 경유지 이내에 도착해야 함
~~~python
def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, K: int) -> int:
        # build adjacency list
        adjList = defaultdict(list)
        for source, dest, price in flights:
            adjList[source].append([dest, price])

        visited = {src: 0}  # city: minimum price to get here
        queue = deque([(src, 0, 0)])
        # BFS start with src
        # queue : (city, curPrice, curStops)
        while queue:
            # get curCity and curPrice, and curStops
            curCity, curPrice, curStops = queue.popleft()
            for newCity, travelCost in adjList[curCity]:
                if newCity not in visited or travelCost + curPrice < visited[newCity]:
                    # append to queue if current stops < K
                    if curStops < K:
                        queue.append((newCity, travelCost + curPrice, curStops + 1))
                    # add/update to visited
                    visited[newCity] = travelCost + curPrice

        if dst in visited:
            return visited[dst]
        return -1
~~~

## chapter14 트리
- 계층형 트리 구조를 시뮬레이션 하는 추상 자료형(ADT)로, 루트 값과 부모-자식 관계에서 서브트리로 구성되며, 서로 연결된 노드의 집합
- 트리 구조는 우리 주변 일상에서 쉽게 볼 수 있는 위아래 개념을 컴퓨터에서 표현한 구조
- 좀 더 중요한 트리의 속성 중 하나는 재귀로 정의된(Recursively Defined) 자기 참조 자료구조라는 점
- 즉, 트리는 자식도 트리고, 또 그 자식도 트리임. 즉 여러 개의 트리가 쌓아 올려져 큰 트리가 됨
- 흔히 서브트리로 구성된다고 표현하는데, 앞서 트리에 대한 위키피디아의 정의에도 서브트리라는 용어가 등장함

### 트리의 각 명칭
- 트리는 항상 루트(root)에서부터 시작됨. 루트는 자식(child) 노드를 가지며, 간선(Edge)으로 연결되어 있음
- 자식 노드의 개수는 차수(Degree)라고 하며, 크기(Size)는 자신을 포함한 모든 자식 노드의 개수임
- 높이(Height)는 현재 위치에서부터 리프(Leaf)까지의 거리, 깊이(Depth)는 루트에서부터 현재 노드까지의 거리
- 일반적으로 레벨 0(트리)에서부터 시작함. 논문에 따라 1에서부터 시작하는 경우도 있으나 현재 대부분의 문서에서는 0에서부터 시작하는 것이 좀 더 일반적

### 그래프 vs 트리
- 그래프와 트리의 가장큰 차이는 <b>트리는 순환 구조를 갖지 않는 그래프</b>라는 점
- 또한 단방향과 양방향을 모두 가리킬 수 있는 그래프와는 달리, 트리는 부모 노드에서 자식 노드를 가리키는 단방향뿐
- 또한 트리는 부모도 하나, 루트도 하나여야 함

### 이진 트리
- 트리 중에서도 가장 널리 사용되는 트리 자료구조는 이진 트리와 이진 탐색 트리임
- 각 노드가 m개 이하의 자식 노드를 가지고 있는 경우는 m-ary 트리(다항트리, 다진트리)라고 함
- m=2일 경우, 모든 노드의 차수가 2 이하일 때는 특히 이진 트리라고 구분해서 부름
- 이진 트리는 왼쪽, 오른쪽 최대 2개의 자식을 갖는 특별한 형태로 다진 트리에 비해 훨씬 간결할 뿐만 아니라 여러 가지 알고리즘을 구현하는 일도 좀 더 간단하게 처리할 수 있어, 보통 트리라고 하면 특별한 경우가 아니고서는 대부분 이진 트리를 일컬음 
- 이진 트리의 명칭은 논문마다 조금씩 다르므로, 여기서는 되도록 널리 쓰이는 형태로 언급함
- 정 이진 트리(Full Binary Tree): 모든 노드가 0개 또는 2개의 자식 노드를 갖음
- 완전 이진 트리(Complete Binary Tree): 마지막 레벨을 제외하고 모든 레벨이 완전히 채워져 있으며 마지막 레벨의 모든 노드는 가장 왼쪽부터 채워져 있음
- 포화 이진 트리(Perfect Binary Tree): 모든 노드가 2개의 자식 노드를 갖고 있으며, 모든 리프 노드가 동일한 깊이 또는 레벨을 가짐. 문자 그대로, 가장 완벽한(Perfect) 유형의 트리

### 이진 트리의 최대 깊이 구하기

