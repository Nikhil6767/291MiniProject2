from pymongo import MongoClient
import sys

def search_titles():
	return

def search_genres():
	return

def search_cast():
	return

def add_movie():
	return

def add_case():
	return

if __name__ == "__main__":

	if len(sys.argv) != 2:
		print("Usage: python3 miniproject2.py port_num")
		exit()

	# get the port num
	port_num = int(sys.argv[1])
	# connect to server
	client = MongoClient('localhost', port_num)

	# open database
	db = client["291db"]