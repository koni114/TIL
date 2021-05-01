class MyClass:
    def __init__(self):
        self.alligator = 'hatching'
        self.elephant = 'calf'

a = MyClass()
for key, value in a.__dict__.items():
    print(f'{key} = {value}')