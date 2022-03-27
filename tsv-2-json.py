# adapted from https://www.geeksforgeeks.org/python-tsv-conversion-to-json/
import json

def tsv2json(input_file,output_file):
    arr = []
    file = open(input_file, 'r')
    a = file.readline()
      
    # The first line consist of headings of the record 
    # so we will store it in an array and move to 
    # next line in input_file.
    titles = [t.strip() for t in a.split('\t')]
    for line in file:
        d = {}
        for t, f in zip(titles, line.split('\t')):
            print("t is ", t)
            print("f is ", f)
            if t == "primaryProfession" or t == "knownForTitles" or t == "genres" or t == "characters":
                f = f.strip()
                f = f.split(",")
                
                d[t] = f
            else:
                # Convert each row into dictionary with keys as titles
                d[t] = f.strip()
        # we will use strip to remove '\n'.
        arr.append(d)
          
        # we will append all the individual dictionaires into list 
        # and dump into file.
    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(json.dumps(arr, indent=4))
 

in_file = ["name.basics.tsv", "title.basics.tsv", "title.principals.tsv", "title.ratings.tsv"]
out_file = ["name.basics.json", "title.basics.json", "title.principals.json", "title.ratings.json"]

for i in range(len(in_file)):
	tsv2json(in_file[i], out_file[i])
