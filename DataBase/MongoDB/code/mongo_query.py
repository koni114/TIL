from pprint import pprint
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["test_database"]

collection = db["customer_segment"]

# 1. collection 의 모든 코드 가져오기
results = collection.find()
for document in results:
    print(document)
    
# 2. downloadableUrl 값이 stg-customer-segment-storage 인 document 들의 requestId 값 출력
query = {"downloadableUrl": "stg-customer-segment-storage"}
projection = {"requestId": 1}

results = collection.find(query, projection)
for result in results:
    pprint(result)

# 3. downloadableUrl 값이 dev-customer-segment-storage 인 document 삭제
query = {"downloadableUrl": "dev-customer-segment-storage"}
result = collection.delete_many(query)

# 삭제된 문서 수 출력
print(f"Deleted {result.deleted_count} documents.")

# 4. status field 값이 "REQUESTED" 이면서 
# downloadableUrl field 값이 "dev-customer-segment-storage" 인 document 를 삭제

query = {"status": "REQUESTED", 
         "downloadableUrl": "dev-customer-segment-storage"}
result = collection.delete_many(query)
print(f"Deleted {result.deleted_count} documents.")

# 5. downloadableUrl 필드의 리스트의 길이가 3개인 것들만 select
query = {"downloadableUrl": {"$size": 3}}
results = collection.find(query)

# 6. downloadableUrl 리스트 내 값이 "dev-customer-segment-storage" 인 것들을 모두 
# "stg-customer-segment-storage" 로 update

# 업데이트 쿼리 및 업데이트 작업 정의
query = {"downloadableUrl": "dev-customer-segment-storage"}
update = {"$set": {"downloadableUrl.$": "stg-customer-segment-storage"}}

result = collection.update_many(query, update)

# 업데이트된 문서 수 출력
print(f"Matched {result.matched_count} documents and modified {result.modified_count} documents.")