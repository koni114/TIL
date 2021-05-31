from pymongo import MongoClient
import datetime
import pprint
# DB 연결
#- 방법1 - URL
mongodb_URI = "mongodb://localhost:27017"
client = MongoClient(mongodb_URI)

#- 방법2 - IP, PORT
client = MongoClient('localhost', 27017)
print(client.list_database_names())

print(client.list_database_names())  #- database list

#- db 접근
db = client['transaction']
collection = db['bunjang']

post = {"seller_location":"test",
"category":"test",
"title":"test",
"price":"test",
"time":"test",
"main_contents":"test",
"like":"test",
"click_number":"test",
"item_image":"test",
"user_id":"test",
"number_of_seller_product":"test"}
post_id = collection.insert_one(post).inserted_id  #- Collection insert

pprint.pprint(collection.find_one())                  #- Collection 내 단일 Document 조회
collection.find_one({'author':'Mike'})                #- 쿼리를 통한 Document 조회
pprint.pprint(collection.find_one({"_id":post_id}))   #- post_id를 통한 조회

#- 여러 Document 추가 - insert_,many() 메서드 이용

new_posts = [

    {
        "author": "Mike",
        "text": "Another post!",
        "tags": ["bulk", "insert"],
        "date": datetime.datetime(2009, 11, 12, 11, 14)
    },

    {
        "author": "Eliot",
        "title": "MongoDB is fun",
        "text": "and pretty easy too!",
        "date": datetime.datetime(2009, 11, 10, 10, 45)
    }

]

result = collection.insert_many(new_posts)
result.inserted_ids

#- Document 조회 - find() 메서드 이용
for post in collection.find():
    pprint.pprint(post)

#- counting
collection.count_documents({})                  #- collection 내 도큐먼트 수 조회
collection.count_documents({"author": "Mike"})  #- 쿼리를 통한 도큐먼트 수 조회
