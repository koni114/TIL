from pprint import pprint
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["test_database"]

collection = db["customer_segment"]

# 1. segment 내 key 값이 94f0ce0a-eee0-4b4b-bcd5-f71dd845b974 인 status 값을 PROCESSING 으로 변경
request_id = '94f0ce0a-eee0-4b4b-bcd5-f71dd845b974'
query = {"segment.requestId": request_id}
result = collection.find(query)
pprint(list(result))

# 업데이트할 내용
update = {
    "$set": {"segment.$.status": "PROCESSING"}
    }

result = collection.update_one(query, update)

# 2. segment 필드 안의 keywords 의 값이 ["Tech", "Flipboard", "Techcrunch", "Feedly"] 인 리스트의 값만 추출하고 싶습니다.
# 쿼리 작성
query = {"segment": {"$elemMatch":{"keywords": ["Tech", 
                              "Flipboard", 
                              "Techcrunch", 
                              "Feedly"]
                                   }
}}

projection = {"downloadableUrl": 1,
              "segment": {"$elemMatch":{"keywords": ["Tech", 
                              "Flipboard", 
                              "Techcrunch", 
                              "Feedly"]
                                   }
                }
              }

documents = collection.find(query, projection)

for doc in documents:
    pprint("##########")
    pprint(doc)