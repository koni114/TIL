"""
URL 구문 분석
- URL 구문 분석 함수는 URL 문자열을 구성 요소로 분할하거나 URL 구성 요소를 URL 문자열로 결합하는데 중점을 둠

scheme, 0, URL 스킴 지정자, scheme 매개 변수
netloc, 1, 네트워크 위치 부분, 빈 문자열
path, 2, 계층적 경로, 빈 문자열
params, 3, 마지막 경로 요소의 파라미터, 빈 문자열
query, 4, 퀴리 구성 요소, 빈 문자열
fragment, 5, 프래그먼트 식별자, 빈 문자열
username, 사용자 이름, None
password, 비밀 번호, None
hostname, 호스트 이름(소문자), None
port, 존재하면, 정수로 표시되는 포트 번호, None
"""

from urllib.parse import urlparse
url_string = "http://www.cwi.nl:80/%7Eguido/Python.html"
parsed_url = urlparse(url_string, scheme='', allow_fragments=True)

print(f"scheme : {parsed_url.scheme}")
print(f"port : {parsed_url.port}")
print(parsed_url.geturl())



