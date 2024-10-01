import redis

# Redis 클라이언트 생성 (기본 설정은 localhost의 포트 6379입니다)
client = redis.StrictRedis(host='localhost', port=6379, db=0)

# 모든 키 가져오기
keys = client.keys('*')

# 바이트 문자열을 문자열로 변환
keys = [key.decode('utf-8') for key in keys]

print("Redis에 저장된 모든 키:")
for key in keys:
    print(key)