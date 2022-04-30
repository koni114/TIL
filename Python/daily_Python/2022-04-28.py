# 2022.04.28.py
# 파이썬 스크립트 실행시 인자값 전달받기.

# sys.argv 의 배열값 안에 포함되어 있음.
# sys.argv[1] 부터 인자값 확인 가능.
import sys
for v in sys.argv[1:]:
    print(v)
