def find(s):
    is_s_in_str = True
    while True:
        check_str = (yield is_s_in_str)
        is_s_in_str = s in check_str



f = find('Python')
next(f)

print(f.send('Hello, Python!'))
print(f.send('Hello, world!'))
print(f.send('Python Script'))

