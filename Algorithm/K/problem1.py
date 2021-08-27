# - 1. 한번만 사용한 첫 문자 찾기
# - 문자열에서 한번만 사용한 문자를 찾고자 함. 문자열은 소문자만 사용함
# - 한번만 사용한 문자 중 먼저 나타난 문자의 인덱스를 리턴해야 함.
# - 인덱스는 1부터 시작함. 한번만 사용한 문자가 없을 경우 -1을 리턴해야 함.
# - ex) s = "statistics"
# - -> [a, c]

def sol(str):
    from collections import defaultdict
    dic = defaultdict(list)
    for idx, char in enumerate(str):
        dic[char].append(idx)
    for key in dic:
        if len(dic[key]) == 1:
            return dic[key][0] + 1
    return -1

str = "statistics"
str = "ssssaaabcd"
str = "dffasdfasdfsa"
sol(str)
