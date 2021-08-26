A = ['co', 'dil', 'ity']
A = ['abc', 'yyy', 'def', 'csv']
def solution(A):
    from collections import Counter

    #- brute_force 방법을 통한 완전 탐색 구현
    #- 완전 탐색을 통해 문자열 결합시 alphabet count 가 한개라도 2개 이상이면 pass,
    #- 아니면 결합하여 index + 1로 진행
    def check(part_A, idx):
        if idx == len(A):
            return part_A
        result = part_A
        for i in range(idx, len(A)):
            toggle = 0
            tmp_char = result + A[i]
            for v in Counter(tmp_char).values():
                if v > 1:      #- alphabet count > 1 이면 중복 문자 존재. -> pass
                    toggle = 1
                    break
            if toggle == 0:
                tmp = check(tmp_char, idx + 1)
            else:
                tmp = check(part_A, idx + 1)
            result = max(result, tmp, key=len)
        return result
    return len(check("", 0))