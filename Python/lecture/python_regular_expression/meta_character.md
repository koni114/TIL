## 메타 문자란?
- 메타 문자는 특정한 문자 혹은 계열을 표현하는 약속된 기호
- 메타 문자를 이용하면 특정한 규칙을 가진 여러 단어를 짧게 압축할 수 있어 편리
- 메타 문자는 다음과 같이 구성되어 있음

### 메타 문자 구성
- `^`: 문자열의 시작, ex) `^www`는 문자열의 맨 처음에 www가 오는 경우에 매치
- `$`: 문자열의 끝, `.com$`은 문자열의 맨 끝에 `.com`이 오는 경우에 매치
- `|`: or 조건식, 여러 가지 중 하나와 일치하면 매치
- `[]`: 문자 클래스, 대괄호 `[]` 안에 들어있는 문자 중 하나라도 일치하면 매치함 ex) `[abc]`는 a,b,c 중 하나와 매칭됨
- `\d`: 숫자를 나타냄
- `\D`: 숫자가 아닌 모든 문자를 나타냄
- `\w`: 알파벳 대소문자, 숫자, 밑줄(_)을 나타냄
- `\W`: \w에 해당되지 않는 문자들을 나타냄
- `\s`: 공백, 탭 문자와 매칭됨
- `\S`: `\s`에 매칭되지 않는 모든 문자를 나타냄
- `n`: 개행 문자를 나타냄
- `\`: 이스케이프용 문자. 특별한 의미를 나타내는 기호를 문자 그대로 사용할 때 씀 ex $라는 문자를 찾기 위해 `\$`라고 나타내야 함
- `.`: 모든 문자와 대응되는 기호

### 정규표현식(regular expression)이란?
- 복잡한 문자열을 처리할 때 사용되는 도구
- 파이썬은 `re` 모듈이 정규표현식을 지원
- 만약 다음과 같은 문제가 주어졌다고 생각해보자  
  '보안을 위해 고객 정보 중 전화번호 가운데 자리의 숫자는 * 문자로 변경해라'
- 고객 정보는 이름, 주민번호, 전화번호가 문자열 데이터로 주어진다고 가정해보자
```python
text = '''
Elice 123456-1234567 010-1234-5678
Cheshire 345678-678901 01098765432
'''
```
- 이 문제를 정규식을 사용하지 않고 풀려면 매우 복잡하게 풀어야 함
  - 전체 텍스트를 공백 문자를 기준으로 나눔
  - 나누어진 문자열이 전화번호 형식인지 점검
  - 전화번호를 다시 나누어 가운데 자리의 숫자를 `*`로 변환
  - 나눈 문자열을 다시 합쳐 전화번호를 완성 
- 하지만 이러한 문제는 정규 표현식으로 쉽게 해결이 가능

### 정규식 객체
- `re`에는 정규식 객체 개념이 있음
- `re.compile()` 함수는 문자열 패턴을 컴파일하여 정규식 객체를 반환함
- 어떤 정규식을 코드 내에서 여러번 사용할 때 `re.compile()` 함수로 정규식 객체를 만들어 사용
- `re` 모듈의 함수는 `re` 클래스의 함수도 있지만, 정규식 객체에서 호출하기도 함

### re 모듈의 함수
#### 정규식 검사 함수
- 문자열에 대해 정규식으로 검사하는 함수는 대표적으로 `re.match()`, `re.search()`, `re.findall()` ,`re.finditer()` 4가지가 있음
- `re.match(pattern, string)` - string 시작 부분부터 패턴이 존재하는지 검사하여 MatchObject를 반환
- `re.search(pattern, string)`- string 전체에서 pattern이 존재하는지 검사하여 MatchObject를 반환
- `re.findall(pattern, string)` - string 전체에서 패턴과 매치되는 모든 경우를 찾아 list로 반환
- `re.finditer(pattern, string)` - string 전체에서 패턴과 일치하는 결과에 대한 iterator 객체를 반환

#### 문자열 수정 함수
- `re` 모듈에는 패턴과 매치된 문자열을 찾아줄 뿐만 아니라, 편집할 수 있는 함수들도 존재
- `re.sub(pattern, repl, string)` - string에서 pattern과 매칭되는 부분을 repl로 수정한 문자열 반환
- `re.subn(pattern, repl, string)` - `re.sub()`과 동일하지만, 함수의 결과를 (결과 문자열, 교체 횟수) 꼴의 튜플로 반환

### 공백 문자
- 공백 문자(white space)는 스페이스 문자 ''뿐만 아니라 여러 종류가 있음
- `\t`: 가로 탭 문자
- `\n`: 개행 문자
- `\v`: 세로 탭 문자
- `\f`: 용지 넘김 문자
- `\r`: 캐리지 리턴 문자
- 위의 문자들과 모두 매칭되는 정규식 메타 문자는 `\s`, 이를 제외한 문자들과 매칭되는 메타 문자는 `\S`임

### 수량자
- 동일한 글자나 패턴이 반복될 때, 그대로 정규표현식을 만들고자 하면 상당히 불편함
- `\d`, `\w`를 이용하면 각각 숫자와 문자를 한 글자씩 매칭해주는데, 이어지는 문자를 패턴을 만들어, 단어 단위로 매칭하고 싶을 때는 상당히 불편함
- 이런 상황에서 수량자를 배워보자
- `*`: 0개 이상, ex) `elice*` 는 "elic", "elice", "elicee"... 와 매칭
- `+`: 1개 이상, 
- `?`: 0개 또는 1개
- `{n}`: n개
- `{n, m}`: n개 이상, m개 이하
- `{n,}` n개 이상

### 그룹이란 ? 
- 괄호는 그룹을 나타냄. 그룹은 전체 패턴 내에서 하나로 묶어지는 패턴을 말함
- 그룹과 `|`를 결합한 형태, 또는 그룹 뒤에 수량자를 붙이는 패턴으로 자주 사용됨
- `(e|a)lice` --> `elice`, `alice`와 매칭됨
- `(tom|pot)ato` --> `tomato`, `potato`와 매칭됨
- `(base|kick){2}` --> `basebase`, `basekick`, `kickkick`, `kickbase`와 매칭됨

#### 그룹의 재사용
- 한 번 만든 그룹은 재사용할 수도 있음. 만들어진 순서부터 1번부터 시작하는 그룹으로 참조할 수 있는데, 매치한 그룹을 패턴 내에서 재사용하려면 `\\1` 과 같이 그룹 번호를 이스케이프하여 나타내야 함
- 예시 `(to)ma\\1` --> `tomato`와 매칭됨. 괄호를 사용하여 앞에서 만든 그룹 `(to)`를 뒤에서 재사용하는 모습
- 그외 : 이외에도 그룹에는 `re` 모듈의 `match` 객체에 속해있는 group 메서드를 이용하여 매치된 결과 중 일부만을 추출할 수 있는 등 다양한 사용법이 있음