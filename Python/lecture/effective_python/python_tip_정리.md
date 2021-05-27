## python_tip 정리
- 인스턴스의 타입을 check 할 때는 `isinstance` 함수를 응용하자
- f-문자열에서 `:<5`는 공백 5칸 추가, `.2f`는 소수점 2째자리 수
- `sort` 함수에 `key=dict.key` 가 들어가는 것은 딕셔너리의 value로 name을 sorting하겠다는 의미
- `__next__`는 iteration의 순서를 결정짓는 메소드, `__iter__`는 제너레이터를 정의하는 메소드
- `__missing__` 메서드는 딕셔너리에서 키가 없을 때 특정 로직을 처리할 수 있게끔 해주는 함수