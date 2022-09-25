# YAML 작성법
## YAML File 의 장점
- 주석을 넣을 수 있음
- 더 읽기가 편함
- 동일 파일 내에서 '참조'가 가능

## YAML 기본 문법
### 들여쓰기
- 들여쓰기는 기본적으로 2칸 또는 4칸을 지원
~~~YAML
# 2칸 들여쓰기
person:
  name: JaeHun Hur
  job: Developer
  skills:
    - docker
    - kubernetes
~~~
~~~YAML
# 4칸 들여쓰기
person:
    name: Jaehun Hur
    job: Developer
    skills:
        - docker
        - kubernetes
~~~

### 데이터 정의(map)
- 데이터는 `key`:`value` 형식으로 정의
~~~YAML
apiVersion: v1
kind: Pod
metadata:
  name: echo
  labels:
    type: app
~~~
~~~JSON
{
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "name": "echo",
        "labels": {
            "type": "app"
        }
    }
}
~~~

### 주석(comment)
- 주석은 `#`로 표시
~~~YAML
# 전체 라인 주석처리
apiVersion: v1
kind: Pod
metadata:        # 일부 주석 처리
  name: echo
  labels:
    type: app
~~~

### 참/거짓 숫자표현
- 참/거짓은 `true`, `false` 외에 `yes`, `no`를 지원
~~~YAML
study_hard: yes
give_up: no
hello: True
world: TRUE
manual: false
~~~
- 숫자는 정수 또는 실수를 따옴표(`'`) 없이 사용하면 숫자로 인식
~~~YAML
# numbers
version: 1.2

# string
version: "1.2"
~~~

### 줄바꿈(newline)
- 여러 줄을 표현하는 방법
- `|` 지시어는 마지막 줄바꿈이 포함  
  --> last line 다음에 줄바꿈이 포함되어 있는데, 이 줄바꿈이 포함됨
~~~YAML
newlines_sample: |
    number one line

    second line

    last line


# 결과 --> Json
{
  "newlines_sample": "number one line\n\nsecond line\n\nlast line\n"
}
~~~
- `|-` 지시어는 마지막 줄바꿈을 제외  
  --> last line 뒤에 줄바꿈이 포함되어 있지만, 포함되지 않은채로 변환됨
~~~YAML
newlines_sample: |-
            number one line

            second line

            last line

# 결과
{
  "newlines_sample": "number one line\n\nsecond line\n\nlast line"
}
~~~
- `>` 지시어는 중간에 들어간 빈줄을 제외
~~~YAML
newlines_sample: >
            number one line

            second line

            last line

# 결과
{
  "newlines_sample": "number one line\nsecond line\nlast line\n"
}
~~~

## 주의사항
### 띄어쓰기
- key와 value 사이에는 반드시 빈칸이 필요
~~~YAML
# error
key:value

# ok
key: value
~~~

### 문자열 따옴표
- 대부분의 문자열을 따옴표 없이 사용할 수 있지만 `:` 가 들어간 경우는 반드시 따옴표가 필요
~~~YAML
# error
window_drive: c:

# ok
windows_drive: "c:"
windows_drive: 'c:'
~~~

## 참고
### json2yaml
- JSON에 익숙하신 분들을 위한 YAML 변환 사이트  
  https://www.json2yaml.com/
- YAML 문법을 체크하고 어떻게 해석하는지 결과를 알려줌  
  http://www.yamllint.com/
