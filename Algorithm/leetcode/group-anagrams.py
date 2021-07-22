"""
Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
"""
from typing import List
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        from collections import defaultdict
        strs_dict = defaultdict(list)
        for str in strs:
            strs_dict["".join(sorted(str))].append(str)
        return list(strs_dict.values())

s = Solution()
s.groupAnagrams(strs=["eat", "tea", "tan", "ate", "nat", "bat"])

c = ["ccc", "aaaa", "d", "bb"]
sorted(c, key=len)

a = ['cde', 'cfc', 'abc']
def fn(s):
    return s[0], s[-1]

print(sorted(a, key=fn))