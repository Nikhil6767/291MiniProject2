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

	movies = title_basics.find({"$text": {"$search": search}})

	# get the tconst for all the results
	tconst = []
	i = 1
	for movie in movies:
		print(i, movie)
		tconst.append(movie["tconst"])
		i += 1

	if len(tconst) == 0:
		print("No matches found")
		return

	# get movie from user
	pick_mov = True
	while pick_mov:
		movie_choice = int(input("Select a movie or press 0 to return to main menu: "))
		if movie_choice == 0: return
		# check for valid input
		try:
			tconst_find = tconst[movie_choice-1]
		except:
			print("Invalid movie choice, pick again")
			continue
		pick_mov = False

	rating = title_ratings.find({"tconst":tconst_find})
	for rate in rating:
		print('''
rating: {}
number of votes: {}
cast/crew: '''.format(rate["averageRating"], rate["numVotes"]), end = " ")


	names = name_basics.find({"knownForTitles":{"$elemMatch":{"$in":[tconst_find]}}})
	
	for name in names:
		print("name is monke ", name)
		nconst_find = name["nconst"]
		
		characters = title_principals.find({"$and": [{"nconst":nconst_find}, {"tconst": tconst_find}]})
		for char in characters:
			print(name["primaryName"], end = " ")

			for i in range(len(char["characters"])):
				if char["characters"][i] != "\\N" and i != len(char["characters"]) - 1:
					print(char["characters"][i], end = ", ")
				elif char["characters"][i] != "\\N" and i == len(char["characters"]) - 1:
					print(char["characters"][i], end = " ")
				else:
					print(", ", end = " ")

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