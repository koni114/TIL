# 로그를 재정렬해라
# - 로그의 가장 앞부분은 식별자
# - 문자로 구성된 로그가 숫자 로그보다 앞에 옴
# - 식별자는 순서의 영향을 끼치지 않지만, 문자가 동일할 경우 식별자 순으로 함
# - 숫자 로그는 입력 순서대로 함
from typing import List

logs = ["a1 9 2 3 1","g1 act car","zo4 4 7","ab1 off key dog","a8 act zoo"]
# ["let1 art can","let3 art zero","let2 own kit dig","dig1 8 1 5 1","dig2 3 6"]


class Solution:
    def reorderLogFiles(self, logs: List[str]) -> List[str]:
        str_list, num_list = [], []
        for v in logs:
            if v.split(" ")[1].isdigit():
                num_list.append(v)
            else:
                str_list.append(v)

        str_list.sort(key=lambda x: (x.split(" ")[1:], x.split(" ")[0]))
        return str_list + num_list


s = Solution()
s.reorderLogFiles(logs)


