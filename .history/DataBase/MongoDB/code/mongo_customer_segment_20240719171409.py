from pprint import pprint
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["test_database"]

collection = db["customer_segment"]

# 1. segment 내 key 값이 94f0ce0a-eee0-4b4b-bcd5-f71dd845b974 인 status 값을 PROCESSING 으로 변경
request_id = '94f0ce0a-eee0-4b4b-bcd5-f71dd845b974'
query = {"segment.requestId": request_id}
result = collection.find(query)
print(list(result))


# 2. keywords 의 값이 ["Tech", "Flipboard", "Techcrunch", "Feedly"] 인 sub document 값들을 추출
query = {"keywords": [
        "Tech",
        "Flipboard",
        "Techcrunch",
        "Feedly"
      ]}
documents = collection.find(query)

for doc in documents:
    pprint(doc)
    