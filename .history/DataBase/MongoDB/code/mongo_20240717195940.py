from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["test_database"]

collection = db["customer_segment"]

sample_data = {"userId": "jaehun.hur", 
               "query": "Photo, Picsart, B612 키워드를 검색한 이력이 있는 사용자들의 GUID 를 뽑아주세요",
               "requestId": "12333",
               "country_code": ['KOR'],
               "keywords": ['Photo', 'Picsart', 'B612'],
               "rephrase_query": "",
               "status": "REQUSTED", 
               "downloadableUrl": [
                   "genbi-dev",
                   "dev-customer-segment-storage",
                   "12345/result.csv",
                   "12345/result_samples.csv"
               ]}


collection.insert_one(sample_data)


​{
​  "_id" {
​    "$oid": "6642c969772e67db780b9b1a",
​  }
​  "userId": "jinwoo1.seo",
​  "query": "아래 키워드를 검색한 이력이 있는 사용자들의 GUID를 세그별로 뽑아줘. 테크 세그 : Tech, Flipboard, Techcrunch, Feedly, 게임 세그: Game, Playstation, Minecraft, 사진 세그 : Photo, Picsart, B612",  
​  "segment": {
​    "94f0ce0a-eee0-4b4b-bcd5-f71dd845b974": {
​        "sub_query": "'Tech', 'Flipboard', 'Techcrunch', 'Feedly' 키워드를 검색한 이력이 있는 사용자들의 GUID를 뽑아줘",
​        "requestId": "94f0ce0a-eee0-4b4b-bcd5-f71dd845b974",
​        "country_code": ['KOR'],   
​        "keywords": ['Tech', 'Flipboard', 'Techcrunch', 'Feedly'],
​        "rephrase_query": "",
​        "status": "COMPLETED",      
​        "downloadable_url": [
​            "genbi-dev",
​            "test-customer-segment-storage",
​            "bc8236a9-3ab9-4d88-9436-590a54e0d5f4/result.csv"],
​        "answer": ""
​        "createAt": "2024-05-16 10:15:18",
​        "updatedAt": "2024-05-16 10:30:39",
​    },