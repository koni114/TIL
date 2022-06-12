def find(s):
    is_s_in_str = True
    while True:
        check_str = (yield is_s_in_str)
        is_s_in_str = s in check_str

