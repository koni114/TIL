"""
보석과 돌
"""
class Solution:
    def numJewelsInStones(self, jewels: str, stones: str) -> int:
        from collections import defaultdict
        stone_dict = defaultdict(int)
        jewel_num = 0
        for s in stones:
            stone_dict[s] += 1
        for c in jewels:
            jewel_num += stone_dict[c]

        return jewel_num

s = Solution()
s.numJewelsInStones(jewels="aA", stones="aAAbbbb")

class Solution:
    def numJewelsInStones(self, jewels: str, stones: str) -> int:
        from collections import Counter
        count = 0
        freqs = Counter(stones)
        for char in jewels:
            count += freqs[char]

        return count


#- 파이써닉 방법을 통한 문제풀이
class Solution:
    def numJewelsInStones(self, jewels: str, stones: str) -> int:
        return sum(s in jewels for s in stones)

