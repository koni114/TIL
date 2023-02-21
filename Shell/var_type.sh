# -r 읽기 전용 타입(const 라고 보면 됨)
declare -r var1
readonly var1

# -i 정수형 타입
declare -i number
number=3
echo "number = $number"

# -a 배열 타입
declare -a indices

# -A 연관배열(MAP) 타입
declare -A map

# -f 함수 타입
declare -f

# -x 환경변수(export) 저장
declare -x var3  # 스크립트 외부 환경에서도 이 변수를 쓸 수 있게 해줌