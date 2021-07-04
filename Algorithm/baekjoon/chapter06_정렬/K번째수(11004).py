"""
K번째 수
- 수 N개 A1, A2, ..., AN이 주어진다. A를 오름차순 정렬했을 때,
  앞에서부터 K번째 있는 수를 구하는 프로그램을 작성하시오.
- 첫째 줄에 N(1 ≤ N ≤ 5,000,000)과 K (1 ≤ K ≤ N)이 주어진다.
- 둘째에는 A1, A2, ..., AN이 주어진다. (-109 ≤ Ai ≤ 109)
"""
import sys
inf = sys.stdin
N, K = [int(i) for i in sys.stdin.readline().strip().split()]
num_list = [int(i) for i in sys.stdin.readline().strip().split()]
num_list.sort()
print(num_list[K-1])