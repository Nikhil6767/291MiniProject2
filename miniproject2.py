from pymongo import *
import sys

##-- Functions --##
def search_titles(name_basics, title_basics, title_principals, title_ratings):
	# get keywords from the user
	keywords = input("Enter in keywords to search seperated by space: ").split()
	# make index on title and year for searching
	title_basics.create_index([("primaryTitle", "text"), ("startYear", "text")])

	if len(keywords) == 0:
		print("No keywords entered")
		return
	elif len(keywords) == 1:
		search = "\"" + keywords[0] + "\""
	else:
		search = "\"" + keywords[0] + "\"" + " "
		for i in range(1, len(keywords)):
			if i == len(keywords) -1:
				search += "\"" + keywords[i] +"\""
			else:
				search += "\"" + keywords[i] +"\"" + " "

	print(search)

	res = title_basics.find({"$text": {"$search": search}})

	# get the tconst for all the results
	tconst = []
	i = 1
	for r in res:
		print(i, r)
		tconst.append(r["tconst"])
		i += 1

	if len(tconst) == 0:
		print("No matches found")
		return

	# get movie from user
	pick_mov = True
	while pick_mov:
		movie_choice = int(input("Select a movie: "))
		try:
			tconst_find = tconst[movie_choice-1]
		except:
			print("Invalid movie choice, pick again")
			continue
		pick_mov = False

	res = title_ratings.find({"tconst":tconst_find})
	for r in res:
		print('''
rating: {}
number of votes: {}
			'''.format(r["averageRating"], r["numVotes"]))
	
	res = name_basics.find({"knownForTitles":tconst_find})
	for r in res:
		print(r)

	return

def search_genres():
	return

def search_cast():
	return

def add_movie():
	return

def add_cast():
	return

def main_loop(name_basics, title_basics, title_principals, title_ratings):
	loop = True
	while loop:
		print(
			'''
1. Search for titles
2. Search for genres
3. Search for cast/crew members
4. Add a movie
5. Add a cast/crew member
6. End Program
		''')
		user_choice = int(input("Select an option: "))
		if user_choice == 1:
			search_titles(name_basics, title_basics, title_principals, title_ratings)
		elif user_choice == 2:
			search_genres()
		elif user_choice == 3:
			search_cast()
		elif user_choice == 4:
			add_movie()
		elif user_choice == 5:
			add_cast()
		elif user_choice == 6:
			loop = False

##-- MAIN --##
if __name__ == "__main__":
	# check for cmd line args
	if len(sys.argv) != 2:
		print("Usage: python3 miniproject2.py port_num")
		exit()

	# get the port num
	port_num = int(sys.argv[1])
	# connect to server
	client = MongoClient('localhost', port_num)

	# open database
	db = client["291db"]

	# open collections
	name_basics = db["name_basics"]
	title_basics = db["title_basics"]
	title_principals = db["title_principals"]
	title_ratings = db["title_ratings"]

	main_loop(name_basics, title_basics, title_principals, title_ratings)