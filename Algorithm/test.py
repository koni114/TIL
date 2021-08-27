from typing import List
paragraph = "Bob hit a ball, the hit BALL flew far after it was hit."
strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
logs = ['dig1 8 1 5 1', 'let1 art can', 'dig2 3 6', 'let2 own kit dig', 'let3 art zero']

class Solution:
    def groupAnagrams(self, l:List[str]) -> List[List[str]]:
        from collections import defaultdict
        dic = defaultdict(list)
        for word in l:
            dic[''.join(sorted(word))].append(word)
        return list(dic.values())

sol = Solution()
sol.groupAnagrams(l=strs)