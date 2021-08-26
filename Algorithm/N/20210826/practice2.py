#- 동전 뒤집기
#- 동전을 뒤집어서 연속된 앞면(1), 뒷면(0)이 나오게 하는 최소한의 수를 return 하는 문제
#- ex) [1, 1, 0, 0] -> [1, 0, 1, 0] 동전을 총 2번 뒤집어야 함 --> return 2
#- ex) [1, 1, 1, 1] -> [1, 0, 1, 0] 동전을 총 2번 뒤집어야 함
#- ex) [1, 0, 1, 0] -> 0번

#- 제출 소스 코드
def solution(A):
    start_zero_num = 0
    check_num = 0
    for i in range(len(A)):
        if check_num != A[i]:
            start_zero_num += 1
        check_num = 1 - check_num

    start_one_num = 0
    check_num = 1
    for i in range(len(A)):
        if check_num != A[i]:
            start_one_num += 1
        check_num = 1 - check_num

    return min(start_zero_num, start_one_num)

#- 최적화 소스
def solution(A):
    start_zero_num, start_one_num = 0, 0
    toggle_zero, toggle_one = 0, 1

    for i in range(len(A)):
        if toggle_zero != A[i]:
            start_zero_num += 1
        if toggle_one != A[i]:
            start_one_num += 1
        toggle_zero, toggle_one = toggle_one, toggle_zero

    return min(start_zero_num, start_one_num)
