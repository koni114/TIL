"""
몇 개의 항공편으로 연결된 n개의 도시가 있습니다.
항공편[i] = [fromi, toi, pricei]인 배열 항공편이 제공되며,
이는 비용 pricei인 도시 fromi에서 도시 toi로 가는 항공편이 있음을 나타냅니다.

또한 세 개의 정수 src, dst 및 k가 제공되며 최대 k 스톱으로 src에서 dst까지 가장 저렴한 가격을 반환합니다.
그러한 경로가 없으면 -1을 반환합니다.

n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 1
output = 200

Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 0
Output: 500
"""
import heapq
from typing import List
from collections import deque, defaultdict
class Solution:
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

