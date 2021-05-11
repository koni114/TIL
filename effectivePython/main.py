class ValidatingRecord:
    def __init__(self):
        self.exists = 5
    def __getattribute__(self, name):
        #print(f'* 호출: __getattr__({name!r})')
        try:
            value = super().__getattribute__(name)
            #print(f'* {name!r} 찾음, {value!r} 반환')
            return value
        except AttributeError:
            value = f'{name}을 위한 값'
            print(f'* {name!r}를 {value!r}로 설정')
            setattr(self, name, value)
            return value

data = ValidatingRecord()
print('exists: ', data.exists)
print('첫 번째 foo: ', data.foo)
print('두 번째 foo: ', data.foo)
