# 문자열 배열을 받아 애너그램 단위로 그룹핑해라
strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
# [["bat"],["nat","tan"],["ate","eat","tea"]]

from typing import List

test = "eat"
sorted(test)


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        from collections import defaultdict
        sorted_dict = defaultdict(list)
        for s in strs:
            sorted_dict["".join(sorted(s))].append(s)
        return [sorted(v) for _, v in sorted_dict.items()]













