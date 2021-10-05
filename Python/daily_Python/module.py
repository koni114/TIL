# 특정 아이디 문자열 A와 B가 있을 때, 다음 코드를 작성 하십시오.
# 1. '유사도'의 기준을 정의하고, 두 문자열 간의 유사도룰 구하는 코드를 구현 하시오.
# 2.  비교 아이디 문자열을 원본 아이디 문자열과 가장 유사한 순서대로 정렬 하시오.
#
# 유사도 알고리즘 예시: Jaccard Distance
# - J(A, B) = count(교집합) / count(합집합)
#
# 예시)
# 원본 아이디 문자열: "abcd1234"
# 비교 아이디 문자열 리스트: ["abcd", "ab1234", "abxz0011", "1234abcd", "ABCD1234", "abcd1234abcd1234"]


def jaccard_dist(check_s, comp_list):
    simul_list = []

    #- 교집합 / 합집합
    for s in comp_list:
        simul_list.append((s, mk_jac(check_s, s)))

    simul_list = sorted(simul_list, key=lambda x: -x[1])
    return simul_list


def mk_jac(s1, s2):
    s1_set, s2_set = set(s1), set(s2)
    return len(s1_set.intersection(s2_set)) / len(s1_set.union(s2_set))


if __name__ == '__main__':
    check_s = "abcd1234"
    comp_list = ["abcd", "ab1234", "abxz0011", "1234abcd", "ABCD1234", "abcd1234abcd1234"]
    jaccard_dist(check_s, comp_list)






