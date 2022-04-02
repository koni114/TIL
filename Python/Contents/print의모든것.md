# print() 함수 완벽 정리
## built-in 함수 - print 
- `print(*objects, sep= ' ', end='\n', file=sys.stdout, flush=False)`

## print help 내용 정리
~~~python
help(python)

print(...)
    print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)
    
    Prints the values to a stream, or to sys.stdout by default.
    Optional keyword arguments:
    file:  a file-like object (stream); defaults to the current sys.stdout.
    sep:   string inserted between values, default a space.
    end:   string appended after the last value, default a newline.
    flush: whether to forcibly flush the stream.
~~~
- `sep` : 받은 value 사이에 삽입할 문자열을 입력
- `end` : 마지막 value 뒤에 붙이고 싶은 문자열 입력
- `file` : 파일과 같은 객체(= 스트림)를 입력받으며, default 로는 표준출력(= sys.stdout)임  
  `print()` 함수는 기본적으로 objects 를 텍스트 스트림 File로 출력하는 기능을 하는데, 키워드 인자에 write(string) 메서드가 포함된 파일 객체를 설정해주면 출력하는 것 뿐만 아니라 파일에 내용을 쓰는 것도 가능해짐  
  만약 write 메서드가 포함된 파일 객체가 없다면, `file` 의 초기값은 `sys.stdout`으로 설정되어 있음  
  stdout 은 standard out 의 약자로 print() 함수의 기본값은 화면에 내용을 출력하는 것으로 설정되어 있다는 뜻임
~~~python
with open('test1.txt', 'w') as f:
    print("hello world", file=f)
~~~

## flush
- flush: whether to forcibly flush the stream
- 공식 문서에 따르면 일반적으로 출력의 버퍼링 여부는 file에 의해 정해지지만, `flush`를 `True`로 설정하면 스트림이 강제로 flush(clear) 된다고 함
- 즉 print() 함수의 출력 값이 buffered 상태 일 때 `flush=True`로 설정해주면 buffered 된 출력값을 바로 목적지에 도달시킬 수 있음


## 참조 블로그
- https://velog.io/@janeljs/python-print-sep-end-file-flush