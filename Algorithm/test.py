paragraph = "Bob hit a ball, the hit BALL flew far after it was hit."
banned = ["hit"]
from typing import List
class Solution:
    def mostCommonWord(self, paragraph: str, banned: List[str]) -> str:
        import re
        re.sub(r'[^\w]', ' ', paragraph)



        