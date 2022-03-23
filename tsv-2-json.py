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
            
              # Convert each row into dictionary with keys as titles
            d[t] = f.strip()
              
        # we will use strip to remove '\n'.
        arr.append(d)
          
        # we will append all the individual dictionaires into list 
        # and dump into file.
    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(json.dumps(arr, indent=4))
 

in_file = ['title.basics.tsv', 'title.ratings.tsv', 'title.principals.tsv', 'name.basics.tsv']
out_file = ['title.basics.json', 'title.ratings.json', 'title.principals.json', 'name.basics.json']

for i in range(len(in_file)):
	tsv2json(in_file[i], out_file[i])
