#- 문자열이 입력되면, 문자열 한개를 제외하여 사전순으로 가장 빠른 문자열을 반환하는 문제.
#- ex) S = "abc" -> "ab"
def solution(S):
    result = S[1:]
    for i in range(1, len(S)):
        check_str = S[:i] + S[i+1:]
        print(check_str)
        if result > check_str:
            result = check_str
    return result

S = "aeggew"
solution(S)