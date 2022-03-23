import json
from pymongo import MongoClient
import sys

def make_collections(db, col_names):
	collections = []
	for col in col_names:
		# drop if exists
		if col in db.list_collection_names():
			collec = db[col]
			collec.drop()

		# make the collection
		collec = db[col]
		collections.append(collec)

	return collections

def load_data(col_names, collections):

	for i in range(len(col_names)):

		# open the json and get the data
		with open(file_names[i]) as fil:
			data = json.load(fil)

		# insert data into collection
		collections[i].insert_many(data)

if __name__ == "__main__":
	
	if len(sys.argv) != 2:
		print("Usage: python3 load-json.py port_num")
		exit()

	# get the port num
	port_num = int(sys.argv[1])
	# connect to server
	client = MongoClient('localhost', port_num)

	# # create or open database
	db = client["291db"]

	# create the collections
	col_names = ["name_basics", "title_basics", "title_principals", "title_ratings"]
	collections = make_collections(db, col_names)

	# load json data
	file_names = ['name.basics.json', 'title.basics.json', 'title.principals.json', 'title.ratings.json']
	load_data(file_names, collections)