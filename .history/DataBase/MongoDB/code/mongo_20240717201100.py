from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["test_database"]

collection = db["customer_segment"]

results = collection.find()
print(list(results))

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
                       "sql": "SELECT\n  DISTINCT u.guid\nFROM\n  `genbi-dev.gbi_955_mart.cug_917_mart__vmgb_user_basic_info_v3` u\nJOIN\n  `genbi-dev.gbi_955_mart.rbn_795_mart__log_app_usage_hist_v2` a\nON\n  u.guid = a.guid\nWHERE\n  u.country_code = 'KOR'\n  AND u.customer_age BETWEEN 30 AND 39\n  AND a.app_name IN ('com.iwedding.app', 'com.jjlee.wedqueen')\n  AND a.app_usage_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH)\nLIMIT\n  100000;\n",
                       "sqlResponseCount": 880,
                       "codegenChainStatus": 1,
                       "runestoneChainStatus": 1.
                       "createAt": "2024-05-16 10:15:18",
                       "updatedAt": "2024-05-16 10:30:39",
                       },
                   }
               }

collection.insert_one(sample_data)


