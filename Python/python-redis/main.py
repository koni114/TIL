import redis_lock
import redis
import time

client = redis.StrictRedis()
key_list = ['my_lock1', 'my_lock2', 'my_lock3']

for key in key_list: 
    lock_obj = redis_lock.Lock(client, key)
    print(f"lock_obj.locked -> {lock_obj.locked()}")
    if not lock_obj.locked(): 
        with lock_obj:
            # 임계구역 코드 실행
            print(f"락을 획득했습니다. -> {key}")
            time.sleep(20)
            
            print("작업 수행이 완료되었습니다.")
    else:
        print(f"이미 락이 점유중입니다. key -> {key}")