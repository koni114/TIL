"""
ticket[i] = [from, to]가 한 항공편의 출발 및 도착 공항을 나타내는 항공권 목록이 제공됩니다.
여정을 순서대로 재구성하고 반환하십시오.

모든 티켓은 "JFK"에서 출발하는 남성의 것이므로 여정은 "JFK"로 시작해야 합니다.
유효한 여정이 여러 개인 경우 단일 문자열로 읽을 때 사전 순으로 반환 합니다.

예를 들어, 여정 ["JFK", "LGA"]는 ["JFK", "LGB"]보다 어휘 순서가 작습니다.
모든 티켓이 하나 이상의 유효한 일정을 구성한다고 가정할 수 있습니다. 모든 티켓은 한 번만 사용해야 합니다.

다음의 예제 꼭 확인
-  [["JFK","KUL"], ["JFK","NRT"], ["NRT","JFK"]]
-> KUL이 NRT보다 사전순으로는 빠르지만, KUL로 가면 DFS로 연결이 안됨
"""
from typing import List
from collections import OrderedDict
class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        # tickets = [["JFK","SFO"],["JFK","ATL"],
        #            ["SFO","ATL"],["ATL","JFK"],
        #            ["ATL","SFO"]]
        results = []
        from collections import defaultdict
        dic = defaultdict(list)
        for key, value in sorted(tickets):
            dic[key].append(value)

        def dfs(site):
            while dic[site]:
                dfs(dic[site].pop(0))
            results.append(site)

        dfs('JFK')
        return results[::-1]

s = Solution()
test = s.findItinerary([["JFK", "KUL"], ["JFK", "NRT"], ["NRT", "JFK"]])
