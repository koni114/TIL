"""
github 에 민감한 정보를 가리고 올리고 싶을 때, 환경변수 설정
--> dotenv package

SECRET_KEY, PRIVATE_KEY 같이 민감한 정보를 github 에 올리고 싶지 않을 때,
어떻게 하는지 알아보자
"""
import os

# 1. .env 파일을 현재 경로에 만들어줌
f = open(".env", "w")
f.write("PRIVATE_KEY=#as;dlkfja32!")
f.close()

# 2. .gitignore 파일에 해당 파일을 넣어줌
f = open(".gitignore", "w")
f.write(".env")
f.close()

# python-dotenv package 설치
from dotenv import load_dotenv

load_dotenv()
PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
print(PRIVATE_KEY)  # 정상 출력됨을 확인

