import json
import pymongo
import sys

port = sys.argv[1]

client = MongoClient('localhost', port)

db = client["291db"]

# Create the collections in the db
name_basics = db["name_basics"]

clothes.delete_many({})