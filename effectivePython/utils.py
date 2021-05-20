# utils.py
def to_str(data):
    if isinstance(data, str):
        return data
    elif isinstance(data, bytes):
        return data.decode('utf-8')
    else:
        raise TypeError('str이나 bytes를 전달해야 함'
                        f'찾은 값: {data!r}')