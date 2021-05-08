## effective_python 간단정리
### 1-bytes와 str 차이 알아두기
- 파이썬은 문자열 데이터의 시퀀스 표현방법은 두 가지
  - `bytes`, `str`
- bytes 타입의 인스턴스에는 부호가 없는 8바이트 데이터가 그대로 들어감
- str 인스턴스에는 사람이 사용하는 언어의 문자를 표현하는 유니코드 코드 포인트가 들어있음
- 중요한 것은 str 인스턴스에는 직접 대응하는 이진 인코딩이 없고, bytes에는 직접 대응하는 텍스트 인코딩이 없음
- 두 개를 구분하는 help function을 만들어서 적용해야 함
- `bytes`와 `str`는 연산이 불가능함

### 2-str-format 보다는 f-문자열을 사용하자
~~~python
f_string = f'{key:<5} = {value:.2f}'
f'내가 고른 숫자는 {number: .{places}f}'
~~~

### 3-복잡한 식을 쓰지 말고 help function 사용해라
- 파이썬은 복잡한 한줄 식을 사용할 수 있지만 가독성이 좋지 않음 -> 사용 x
- 복잡한 식을 help function으로 만들자

### 4- 인덱스 사용 대신에 언패킹 사용하자
~~~python
snacks = [('베이컨', 350), ('도넛', 240), ('머핀', 190)]
for rank, (name, calories) in enumerate(snacks):
    print(f"{rank} : {name}은 {calories}입니다.")
~~~

### 5- range보다는 enumerate를 사용해라
- range는 가독성이 떨어질 수 있음(ex) `range(len(list))`). 차라리 enumerate 사용하자

### 6- for나 while 루프 뒤에 else 사용하지 말자
- for/while 뒤에 else를 붙여 사용이 가능한데, else는 루프가 끝나자마자 실행됨 
- 조심해야 할 것은 '루프가 정상적으로 완료되지 않으면' else문을 실행해라 가 아님
- 빈 sequence에 대해서 for loop 실행시, else 블록이 바로 실행됨
- else는 동작의 혼동을 줄 수 있으므로 사용하지 말자
~~~python
for i in range(3):
    print(i)
    break
else:
    print("Else block")

>>>
0

for i in []:
    print("Loop", i)
    break
else:
    print("Else block!")

>>>
Else block!
~~~

### 7- 대입식을 사용해 반복을 피하자
- 대입식을 영어로 assignment expression 이라고 하며, 왈러스 연산자라고도 함
- python 3.8부터 도입되었으며, 다음과 같이 사용하며 반복을 피할 수 있음
~~~python
if count := fresh_fruit.get('레몬', 0):
    print(count)
~~~

### 11-시퀀스 슬라이싱 하는 법을 익혀라
- 두 번째 인덱스는 포함되지 않음
- 범위를 지정한 인덱싱은 인덱싱의 범위가 넘어가도 무시됨
- [:]만 사용하면 리스트가 그대로 복사됨

### 12- 스트라이드와 슬라이스를 한 식에 같이 쓰지 말라 
- 스트라이트: 리스트를 일정한 간격을 두고 슬라이싱 할 수 있는 구문

### 13- 슬라이싱보다는 나머지를 모두 잡아내는 언패킹을 사용하자
- 슬라이싱 할 때 인덱싱으로 슬라이싱하면 잘못된 오류로 인해 문제 발생할 여지 있음
- 이 때는 *식(starred expression)을 사용한 언패킹을 사용하자
- 코드가 더 짧고, 인덱스 경계가 어긋나서 오류 날 여지를 줄여줌
~~~python

~~~
