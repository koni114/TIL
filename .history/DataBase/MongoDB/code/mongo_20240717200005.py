from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["test_database"]

collection = db["customer_segment"]

sample_data = {"userId": "jaehun.hur", 
               "query": "아래 키워드를 검색한 이력이 있는 사용자들의 GUID를 세그별로 뽑아줘. 테크 세그 : Tech, Flipboard, Techcrunch, Feedly, 게임 세그: Game, Playstation, Minecraft, 사진 세그 : Photo, Picsart, B612",
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


