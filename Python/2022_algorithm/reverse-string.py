from typing import List


class Solution:
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        i_start, i_end = 0, len(s) - 1
        while i_start <= i_end:
            s[i_start], s[i_end] = s[i_end], s[i_start]
            i_start += 1
            i_end -= 1


s = Solution()
test_list = ["H", "A"]
s.reverseString(s=test_list)
