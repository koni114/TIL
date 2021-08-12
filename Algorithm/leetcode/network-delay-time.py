"""
1에서 n까지 레이블이 지정된 n 노드의 네트워크가 제공됩니다.
또한 시간, 이동 시간의 목록이 지정된 에지 시간[i] = (ui, vi, wi)이 주어집니다.
여기서 ui는 소스 노드, vi는 대상 노드, wi는 신호에 걸리는 시간입니다. 소스에서 타겟으로 이동합니다.

주어진 노드 k에서 신호를 보냅니다. 모든 n 노드가 신호를 수신하는 데 걸리는 시간을 반환합니다.
n개의 모든 노드가 신호를 수신하는 것이 불가능하면 -1을 반환합니다.

times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
times = [[1,2,1]], n = 2, k = 1
times = [[1,2,1]], n = 2, k = 2
"""
import collections
import heapq
import sys
from typing import List
class Solution:
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












