# 금지된 단어를 제외한 가장 흔하게 등장하는 단어를 출력
# 대소문자 구분을 하지 않음. 구두점 또한 무시
from typing import List

paragraph = "a, a, a, a, b,b,b,c, c"
banned = ["a"]


class Solution:
    def mostCommonWord(self, paragraph: str, banned: List[str]) -> str:
        import re
        from collections import Counter
        paragraph = re.sub("[^a-zA-Z]", " ", paragraph)
        paragraph_list = [word.lower() for word in paragraph.split()]

        for k, v in Counter(paragraph_list).most_common():
            if k not in banned:
                return k


s = Solution()
s.mostCommonWord(paragraph=paragraph, banned=banned)