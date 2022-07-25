import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv("/tmp/.env")

user = os.getenv("MONGODB_USER")
pwd = os.getenv("MONGODB_PWD")
host = os.getenv("MONGODB_HOST")
port = os.getenv("MONGODB_PORT")

client = MongoClient(f"mongodb://{user}:{pwd}@localhost:{port}")

db = client.test_db
db.name
db.my_collection
db.list_collection_names()


