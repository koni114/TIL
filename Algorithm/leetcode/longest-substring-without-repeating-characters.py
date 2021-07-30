"""
중복문자가 없는 가장 긴 부분 문자열의 길이 리턴
"""
import itertools


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        from collections import defaultdict
        if not s:
            return 0

        count = 0
        for i, char in enumerate(s):
            char_dict = defaultdict(int)
            char_dict[char] += 1
            count_tmp = 1
            check = i+1
            while check <= len(s)-1:
                if char_dict[s[check]] >= 1:
                    break
                else:
                    char_dict[s[check]] += 1
                    count_tmp += 1
                    check += 1
            count = max(count, count_tmp)

        return count

s = Solution()
s.lengthOfLongestSubstring(s="abcdef")

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        used = {}
        max_length = start = 0
        for index, char in enumerate(s):
            if char in used and start <= used[char]:
                start = used[char] + 1
            else:
                max_length = max(max_length, index - start + 1)
            used[char] = index



