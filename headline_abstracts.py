import requests
import json
import os
import sqlite3
import paralleldots
from ratelimit import limits

# PART 1: Calling the Teleport API (Quality of Life)

# initial call to Teleport API about NYC quality of life
base_url = "https://api.teleport.org/api/urban_areas/slug:new-york/scores/"
r = requests.get(base_url)
d = r.json()

# creating cache dictionary for teleport
dir_path = os.path.dirname(os.path.realpath(__file__))
cache = dir_path + '/' + "nyc_cache.json"
with open(cache, "w") as json_file:
    json.dump(d, json_file)
json_file.close()

# reading cache dictionary contents
cache_file = open(cache, 'r')
cache_contents = cache_file.read()
cache_dict_teleport = json.loads(cache_contents)
cache_file.close()

# score of life in NYC
nyc_score = cache_dict_teleport["teleport_city_score"]

# PART 2: Calling New York Times (NYT) API

"""
NYT API only returns 10 results at a time, so we have to
call it 10 times for a total of 100 results.

SIDENOTE!!!: i'm a bit unsure by the instructions if we need to 
run our code 10 times to get the data or if using a for loop is fine?
"""
# create empty list, check to see if headline is in list, keep adding until 20 and then break

conn = sqlite3.connect("/Users/BinhNguyenAn/Desktop/SI_206/CS/headlines.db")

# creating database
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS Headlines (id INTEGER PRIMARY KEY, Headline TEXT)")
#for headline in lines: #reminder that lines was a variable defined above that is just a list of all of the headlines
#    cur.execute("INSERT INTO Headlines (Headline) VALUES (?)", [headline])

cur.execute("CREATE TABLE IF NOT EXISTS Abstracts (id INTEGER PRIMARY KEY, Abstract TEXT)")
#for abstract in abstract_lines: #reminder that lines was a variable defined above that is just a list of all of the headlines
#    cur.execute("INSERT INTO Abstracts (Abstract) VALUES (?)", [abstract])
#cur.execute("SELECT Headlines.Headline, Abstracts.Abstract FROM Headlines INNER JOIN Abstracts ON Headlines.id = Abstracts.id")

# check 
# writing for loop - it is range 11 instead of 10 because there are repeat headlines that we shouldn't collect twice
headline_list = []
abstract_list = []
tot = 0 

for x in range(11): 
      

    # calling NYT API
    base_url_nyt = "https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=section_name%3A%22New%20York%22&sort=newest&begin_date=20191108&end_date=20191208&page={}&api-key=IeOc9X1YnyZgg5W1JAujzDAKJaG8H1bR".format(x)

    r_nyt = requests.get(base_url_nyt) 
    d_nyt = r_nyt.json()

    # tot += 10

    if tot < 20: 

        for d in d_nyt["response"]["docs"]:
            headline = d["headline"]["main"]
            if headline not in headline_list:
                headline_list.append(headline)
                
            abstract = d["abstract"]
            if abstract not in abstract_list:
                abstract_list.append(abstract) 

        for headline in headline_list:
            cur.execute("SELECT Headline FROM Headlines WHERE Headline = ?", [headline])
            if cur.fetchone() == None: # checks to see if headline is in db
                cur.execute("INSERT INTO Headlines (Headline) VALUES (?)", [headline])
                tot += 1

        for abstract in abstract_list:
            cur.execute("SELECT Abstract FROM Abstracts WHERE Abstract = ?", [abstract])
            if cur.fetchone() == None:
                cur.execute("INSERT INTO Abstracts (Abstract) VALUES (?)", [abstract])

        """if len(headline_list) > 0:
            for headline in headline_list:
                cur.execute("INSERT INTO Headlines (Headline) VALUES (?)", [headline])
            for abstract in abstract_list:
                cur.execute("INSERT INTO Abstracts (Abstract) VALUES (?)", [abstract])"""
    else:
        break

# cur.execute("CREATE TABLE test_table AS SELECT Headlines.Headline, Abstracts.Abstract FROM Headlines INNER JOIN Abstracts ON Headlines.id = Abstracts.id")
conn.commit()
conn.close()

"""cache_nyt = dir_path + '/' + "nyt_cache.json"
    cache_nyt_abstract = dir_path + '/' + "nyt_abstract_cache.json"

    # checks if cache exists
    if os.path.isfile(cache_nyt) and os.path.isfile(cache_nyt_abstract):

        # checks if file has 100 lines - if not, keep adding
        cache_nyt_read = open(cache_nyt, "r")
        lines = cache_nyt_read.readlines()

        cache_nyt_abstract_read = open(cache_nyt_abstract, "r")
        abstract_lines = cache_nyt_abstract_read.readlines()

        # if len(lines) < 100:
        r_nyt = requests.get(base_url_nyt) 
        d_nyt = r_nyt.json()
            # appending more lines to file
        cache_nyt_file = open(cache_nyt, "a")
        cache_nyt_abstract_file = open(cache_nyt_abstract, "a")

        if tot < 20: 

            for d in d_nyt["response"]["docs"]:
                headline = d["headline"]["main"]
                if headline not in headline_list:
                    headline_list.append(headline)
                    tot += 1
                
                abstract = d["abstract"]
                if abstract not in abstract_list:
                    abstract_list.append(abstract)
                    tot += 1

                if headline not in lines:
                    cache_nyt_file.write(headline)
                    cache_nyt_file.write("\n")
            
                if abstract not in abstract_lines:
                    cache_nyt_abstract_file.write(abstract)
                    cache_nyt_abstract_file.write("\n")
        
            

        else:
            break

        cache_nyt_file.close()
        cache_nyt_read.close()
        cache_nyt_abstract_file.close()
        cache_nyt_abstract_read.close()        

    else:
        r_nyt = requests.get(base_url_nyt) 
        d_nyt = r_nyt.json()

        # creating cache for NYT files
        cache_nyt_file = open(cache_nyt, "w")
        for d in d_nyt["response"]["docs"]:
            headline = d["headline"]["main"]
            cache_nyt_file.write(headline)
            cache_nyt_file.write("\n")
        cache_nyt_file.close()

        cache_nyt_abstract_file = open(cache_nyt_abstract, "w")
        for d in d_nyt["response"]["docs"]:
            abstract = d["abstract"]
            cache_nyt_abstract_file.write(abstract)
            cache_nyt_abstract_file.write("\n")
        cache_nyt_abstract_file.close()"""

""" ignore this
# reading cache dictionary contents
cache_file_nyt = open(cache_nyt, 'r')
cache_contents_nyt = cache_file_nyt.read()
cache_dict_nyt= json.loads(cache_contents_nyt)
cache_file_nyt.close()"""

# PART 3: Calling the Parallel Dots (word sentiment analyzer) API

# PART 4: Creating the Headlines and Abstract database

# CHANGE THIS TO YOUR OWN DIRECTORY!!!!


"""# creating database
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS Headlines (id INTEGER PRIMARY KEY, Headline TEXT)")
for headline in lines: #reminder that lines was a variable defined above that is just a list of all of the headlines
    cur.execute("INSERT INTO Headlines (Headline) VALUES (?)", [headline])

cur.execute("CREATE TABLE IF NOT EXISTS Abstracts (id INTEGER PRIMARY KEY, Abstract TEXT)")
for abstract in abstract_lines: #reminder that lines was a variable defined above that is just a list of all of the headlines
    cur.execute("INSERT INTO Abstracts (Abstract) VALUES (?)", [abstract])
cur.execute("SELECT Headlines.Headline, Abstracts.Abstract FROM Headlines INNER JOIN Abstracts ON Headlines.id = Abstracts.id")
cur.execute()
# cur.execute("CREATE TABLE test_table AS SELECT Headlines.Headline, Abstracts.Abstract FROM Headlines INNER JOIN Abstracts ON Headlines.id = Abstracts.id")
conn.commit()
conn.close()"""







