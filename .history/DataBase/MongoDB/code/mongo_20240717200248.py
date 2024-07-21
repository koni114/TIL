from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["test_database"]

collection = db["customer_segment"]

sample_data = {"userId": "jaehun.hur", 
               "query": "아래 키워드를 검색한 이력이 있는 사용자들의 GUID를 세그별로 뽑아줘. 테크 세그 : Tech, Flipboard, Techcrunch, Feedly, 게임 세그: Game, Playstation, Minecraft, 사진 세그 : Photo, Picsart, B612",
               "segment": {
                   "94f0ce0a-eee0-4b4b-bcd5-f71dd845b974": {
                       "sub_query": "'Tech', 'Flipboard', 'Techcrunch', 'Feedly' 키워드를 검색한 이력이 있는 사용자들의 GUID를 뽑아줘",
                       "requestId": "94f0ce0a-eee0-4b4b-bcd5-f71dd845b974",
                       "country_code": ['KOR'],
                       "keywords": ['Tech', 'Flipboard', 'Techcrunch', 'Feedly'],
                       "rephrase_query": "",
                       "status": "COMPLETED",
                       "downloadable_url": [
                           "genbi-dev",
                           "test-customer-segment-storage",
                           "bc8236a9-3ab9-4d88-9436-590a54e0d5f4/result.csv"],
                       "answer": "",
                       "createAt": "2024-05-16 10:15:18",
                       "updatedAt": "2024-05-16 10:30:39",
                       },
                   }
               }

collection.insert_one(sample_data)


