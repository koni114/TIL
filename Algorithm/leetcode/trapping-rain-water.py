"""
빗물 트래핑
- 높이를 입력받아 비 온 후 얼마나 많은 물이 쌓일 수 있는지를 계산하여라
- 확인해야 할 것
  - left <= right 등호 들어가야 하는가?
  - height = 0  예외처리 --> 0
"""
from typing import List
class Solution:
    def trap(self, height: List[int]) -> int:
        if not height:
            return 0

        left, right = 0, len(height)-1
        left_max, right_max = height[left], height[right]
        volume = 0

        while left <= right:
            left_max, right_max = max(left_max, height[left]), max(right_max, height[right])

            if left_max <= right_max:
                volume += left_max - height[left]
                left += 1
            else:
                volume += right_max - height[right]
                right -= 1

        return volume

s = Solution()

#- stack 풀이 ***
class Solution:
    def trap(self, height: List[int]) -> int:
        stack = []
        volume = 0

        for i in range(len(height)):
            while stack and height[i] > height[stack[-1]]:
                top = stack.pop()
                if not stack:
                    break

                distance = i - stack[-1] - 1
                waters = min(height[i], height[stack[-1]]) - height[top]
                volume += distance * waters
            stack.append(i)

        return volume

s = Solution()
s.trap([0,1,0,2,1,0,1,3,2,1,2,1])