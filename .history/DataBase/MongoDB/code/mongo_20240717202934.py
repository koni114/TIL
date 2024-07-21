from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["test_database"]

collection = db["customer_segment"]

sample_data = {"userId": "jaehun.hur", 
               "query": "아래 키워드를 검색한 이력이 있는 사용자들의 GUID를 세그별로 뽑아줘. 테크 세그 : Tech, Flipboard, Techcrunch, Feedly, 게임 세그: Game, Playstation, Minecraft, 사진 세그 : Photo, Picsart, B612",
               "segment": {
                   "94f0ce0a-eee0-4b4b-bcd5-f71dd845b974": {
                       "subQuery": "'Tech', 'Flipboard', 'Techcrunch', 'Feedly' 키워드를 검색한 이력이 있는 사용자들의 GUID를 뽑아줘",
                       "requestId": "94f0ce0a-eee0-4b4b-bcd5-f71dd845b974",
                       "countryCode": ['KOR'],
                       "keywords": ['Tech', 'Flipboard', 'Techcrunch', 'Feedly'],
                       "rephraseQuery": "",
                       "status": "COMPLETED",
                       "downloadableUrl": [
                           "genbi-dev",
                           "test-customer-segment-storage",
                           "bc8236a9-3ab9-4d88-9436-590a54e0d5f4/result.csv"],
                       "answer": "\n\n\n**Source 1**. 고객 선호도 기반 세그먼트 추출\n\n -API 검색 키워드: ['lg강남본점']\n\n**Source 2**. 고객 프로파일, 제품 보유, 앱 사용 이력 기반 세그먼트 추출\n\n -SQL 생성 질의: 한국에서 최근 세달 동안 '아이웨딩', '웨딩의여신'앱을 쓴 30대 고객 알려줘\n```sql\nSELECT\n  DISTINCT u.guid\nFROM\n  `genbi-dev.gbi_955_mart.cug_917_mart__vmgb_user_basic_info_v3` u\nJOIN\n  `genbi-dev.gbi_955_mart.rbn_795_mart__log_app_usage_hist_v2` a\nON\n  u.guid = a.guid\nWHERE\n  u.country_code = 'KOR'\n  AND u.customer_age BETWEEN 30 AND 39\n  AND a.app_name IN ('com.iwedding.app', 'com.jjlee.wedqueen')\n  AND a.app_usage_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH)\nLIMIT\n  100000;\n\n```\n\n\n위 조건을 만족하는 최종 고객 세그먼트 요청 현황 및 다운로드 버튼을 아래 좌측 Cloud Icon 버튼을 통해 확인하실 수 있습니다.\n",
                       "sql": "SELECT\n  DISTINCT u.guid\nFROM\n  `genbi-dev.gbi_955_mart.cug_917_mart__vmgb_user_basic_info_v3` u\nJOIN\n  `genbi-dev.gbi_955_mart.rbn_795_mart__log_app_usage_hist_v2` a\nON\n  u.guid = a.guid\nWHERE\n  u.country_code = 'KOR'\n  AND u.customer_age BETWEEN 30 AND 39\n  AND a.app_name IN ('com.iwedding.app', 'com.jjlee.wedqueen')\n  AND a.app_usage_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH)\nLIMIT\n  100000;\n",
                       "sqlResponseCount": 880,
                       "codegenChainStatus": 1,
                       "runestoneChainStatus": 1,
                       "createAt": "2024-05-16 10:15:18",
                       "updatedAt": "2024-05-16 10:30:39",
                       },
                   "d2b0e193-d048-4ac4-bfd6-8c869a6319fe": {
                       "subQuery": "'Game', 'Playstation', 'Minecraft' 키워드를 검색한 이력이 있는 사용자들의 GUID를 뽑아줘",
                       "requestId": "d2b0e193-d048-4ac4-bfd6-8c869a6319fe",
                       "countryCode": ['KOR'],
                       "keywords": ['Game', 'Playstation', 'Minecraft'],
                       "rephraseQuery": "",
                       "status": "COMPLETED",
                       "downloadableUrl": [
                           "genbi-dev",
                           "test-customer-segment-storage",
                           "d2b0e193-d048-4ac4-bfd6-8c869a6319fe/result.csv"],
                       "answer": "\n\n\n**Source 1**. 고객 선호도 기반 세그먼트 추출\n\n -API 검색 키워드: ['lg강남본점']\n\n**Source 2**. 고객 프로파일, 제품 보유, 앱 사용 이력 기반 세그먼트 추출\n\n -SQL 생성 질의: 한국에서 최근 세달 동안 '아이웨딩', '웨딩의여신'앱을 쓴 30대 고객 알려줘\n```sql\nSELECT\n  DISTINCT u.guid\nFROM\n  `genbi-dev.gbi_955_mart.cug_917_mart__vmgb_user_basic_info_v3` u\nJOIN\n  `genbi-dev.gbi_955_mart.rbn_795_mart__log_app_usage_hist_v2` a\nON\n  u.guid = a.guid\nWHERE\n  u.country_code = 'KOR'\n  AND u.customer_age BETWEEN 30 AND 39\n  AND a.app_name IN ('com.iwedding.app', 'com.jjlee.wedqueen')\n  AND a.app_usage_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH)\nLIMIT\n  100000;\n\n```\n\n\n위 조건을 만족하는 최종 고객 세그먼트 요청 현황 및 다운로드 버튼을 아래 좌측 Cloud Icon 버튼을 통해 확인하실 수 있습니다.\n",
                       "sql": "SELECT\n  DISTINCT u.guid\nFROM\n  `genbi-dev.gbi_955_mart.cug_917_mart__vmgb_user_basic_info_v3` u\nJOIN\n  `genbi-dev.gbi_955_mart.rbn_795_mart__log_app_usage_hist_v2` a\nON\n  u.guid = a.guid\nWHERE\n  u.country_code = 'KOR'\n  AND u.customer_age BETWEEN 30 AND 39\n  AND a.app_name IN ('com.iwedding.app', 'com.jjlee.wedqueen')\n  AND a.app_usage_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH)\nLIMIT\n  100000;\n",
                       "sqlResponseCount": 100,
                       "codegenChainStatus": 1,
                       "runestoneChainStatus": 1,
                       "createAt": "2024-05-16 10:15:18",
                       "updatedAt": "2024-05-16 10:30:39",
                       },
                   }
               }

collection.insert_one(sample_data)


