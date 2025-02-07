from numpy import char
from pymongo import *
import sys

##-- Functions --##
def search_titles(name_basics, title_basics, title_principals, title_ratings):
	# get keywords from the user
	keywords = input("Enter in keywords to search seperated by space: ").split()

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

	# find the matches
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

	# get the ratings and votes
	rating = title_ratings.find({"tconst":tconst_find})
	for rate in rating:
		print('''
rating: {}
number of votes: {}
cast/crew: '''.format(rate["averageRating"], rate["numVotes"]))

	# find the nconsts of the cast
	nconst = []
	casts = title_principals.find({"tconst":tconst_find})
	for cast in casts:
		nconst.append(cast["nconst"])

	# find the names of cast
	for n in nconst:
		names = name_basics.find_one({"nconst": n})
		print(names["primaryName"], "who plays", end = " ")

		# find the characters played
		casts = title_principals.find_one({"$and": [{"nconst":n}, {"tconst": tconst_find}]})
		for i in range(0, len(casts["characters"])):
			
			if casts["characters"][i] == "\\":
				print("no one")

			elif casts["characters"][i] != "N" and i != len(casts["characters"]) - 1:
				print(casts["characters"][i], end = ", ")

			elif casts["characters"][i] != "N" and i == len(casts["characters"]) - 1:
				print(casts["characters"][i])
		
	return

def search_genres(title_basics, title_ratings):
	try:
		genre = input("enter a genre: ")
		genre = "\"" + genre + "\""
		min_count = int(input("enter minimum vote count: "))
	except:
		print("invalid inputs... exiting")
		return
	
	print("loading...")

	result = []

	# find all movies that have specified genre
	movies = title_basics.find({"$text": {"$search": genre}})
	mt = []
	for movie in movies:
		mt.append(movie["tconst"])
		# find movies with numVotes greater than specifies min_count

	rating = title_ratings.find({
  									"numVotes": {
    								"$gte": min_count
  									}
									})
		
	for r in rating:
		if r["tconst"] in mt:
			movies = title_basics.find_one({"tconst": r["tconst"]})
			result.append([r["numVotes"], movies["primaryTitle"]])
		
	for r in sorted(result, reverse=True):
		print(r[1] + ", votes: " + str(r[0]))

	

def search_cast(name_basics, title_basics, title_principals):
	try:
		name = input("enter a cast/crew name: ")
		name = "\"" + name + "\""
	except:
		print("invalid inputs... exiting")

	# first find cast based on name to find professions
	names = name_basics.find({"$text": {"$search": name}})
	for n in names:
		print(n["primaryName"])
		print("professions: ")
		for proffesion in n["primaryProfession"]:
			print(proffesion)
		# then find job and characters info using nconst
		titleps = title_principals.find({"$text": {"$search": n["nconst"]}})
		for titlep in titleps:
			print("title:")
			# finally find title using tconst
			title = title_basics.find({"$text": {"$search": titlep["tconst"]}})
			for t in title:
				print(t["primaryTitle"])
			print("job:")
			# do a check if job is null
			job = titlep["job"]
			job = job.strip('\\')
			if job != "N":
				print(job)
			else:
				print("not available")
			print("character:")
			# do a check if character is null
			character = titlep["characters"]
			try:
				character.strip('\\')
				# if we are here then there is no list of characters
				print("not available")
			except:
				for c in titlep["characters"]:
					print(c)


def add_movie(title_basics):
	id = input("enter a unique id: ")

	unique = title_basics.find({"$text": {"$search": id}})
	
	# check if id is unique
	count = 0
	for u in unique:
		count += 1
	if count == 0:
		print("id is unique... continuing")
	else:
		print("id is not unique... exiting")
		return
	
	title = input("enter movie title: ")
	s_year = input("enter start year: ")
	r_time = input("enter the running time: ")
	genres = input("enter space seperated all genres for the movie: ").split(" ")

	# insert info
	title_basics.insert_one({"tconst": id,
							 "titleType": "movie",
							 "primaryTitle": title,
							 "originalTitle": title,
							 "isAdult": "\\N",
							 "startYear": s_year,
							 "endYear": "\\N",
							 "runtimeMinutes": r_time,
							 "genres": genres})

	print("done adding movie... exiting")


def add_cast(name_basics, title_basics, title_principals, title_ratings):
	print("preparing...")

	tid = input("enter existing title id: ")
	unique = title_basics.find({"$text": {"$search": tid}})

	# check if title id exists
	count = 0
	for u in unique:
		count += 1
	if count == 0:
		print("title id is not in database... exiting")
		return
	else:
		print("title id is in database... continuing")


	nid = input("enter existing cast/crew member id: ")
	unique = name_basics.find({"$text": {"$search": nid}})

	# check if persons id exists
	count = 0
	for u in unique:
		count += 1
	if count == 0:
		print("persons id is not in database... exiting")
		return
	else:
		print("persons id is in database... continuing")
	

	cat = input("enter a category: ")
	
	# find largest orderings
	ords = title_principals.find({"$text": {"$search": tid}}).sort("ordering", -1).limit(1)
	for o in ords:
		# insert info
		title_principals.insert_one({"tconst": tid,
								"ordering": o["ordering"] + 1,
								"nconst": nid,
								"category": cat,
								"job": "\\N",
								"characters": "\\N"})

		print("done adding cast/crew... exiting")
		return

	# if we are here then that means that the title id is not yet in title_principals
	# insert info
	title_principals.insert_one({"tconst": tid,
							"ordering": 1,
							"nconst": nid,
							"category": cat,
							"job": "\\N",
							"characters": "\\N"})

	print("done adding cast/crew... exiting")



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
			search_genres(title_basics, title_ratings)
		elif user_choice == 3:
			search_cast(name_basics, title_basics, title_principals)
		elif user_choice == 4:
			add_movie(title_basics)
		elif user_choice == 5:
			add_cast(name_basics, title_basics, title_principals, title_ratings)
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