from pprint import pprint
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["test_database"]

collection = db["customer_segment"]

# segment 내 key 값이 94f0ce0a-eee0-4b4b-bcd5-f71dd845b974 인 status 값을 DOWNLOADABLE 로 변경
request_id = '94f0ce0a-eee0-4b4b-bcd5-f71dd845b974'
query = {f"segment.{request_id}": {"$exists": True}}
update = {"$set": {"segment.94f0ce0a-eee0-4b4b-bcd5-f71dd845b974.status": "DOWNLOADABLE"}}
