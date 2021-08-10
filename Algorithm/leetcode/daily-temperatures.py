"""
- 매일 화씨 온도 리스트 T를 입력받아서,
  더 따뜻한 날씨를 위해서는 며칠을 더 기다려야 하는지를 출력
"""
from typing import List
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        result = [0] * len(temperatures)
        stack = [0]

        for idx, value in enumerate(temperatures[1:], 1):
            while stack and temperatures[stack[-1]] < value:
                tmp_idx = stack.pop()
                result[tmp_idx] = idx - tmp_idx
            stack.append(idx)

        return result

s = Solution()
s.dailyTemperatures([30, 60, 90])