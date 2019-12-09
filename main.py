import requests
import json
import os
import sqlite3

"""conn = sqlite3.connect("/Users/BinhNguyenAn/cs.db")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS CS")
cur.execute("CREATE TABLE CS (Headline TEXT, Sentiment INTEGER, Quality of Life INTEGER)")
cur.execute("INSERT INTO CS (Headline, Sentiment, Quality of Life) VALUES (?,?,?)", FIX, FIX, nyc_score)
conn.commit()
conn.close()"""


# initial call to Teleport API about NYC quality of life
base_url = "https://api.teleport.org/api/urban_areas/slug:new-york/scores/"
r = requests.get(base_url)
d = r.json()

# creating cache dictionary for teleport
dir_path = os.path.dirname(os.path.realpath(__file__))
cache = dir_path + '/' + "nyc_cache.json"
with open(cache, "w") as json_file:
    json.dump(d, json_file)

# reading cache dictionary contents
cache_file = open(cache, 'r')
cache_contents = cache_file.read()
cache_dict_teleport = json.loads(cache_contents)
cache_file.close()

# score of life in NYC
nyc_score = cache_dict_teleport["teleport_city_score"]

"""
NYT API only returns 10 results at a time, so we have to
call it 10 times for a total of 100 results.
"""

def duplicates(headline, filename):
    f = open(filename, "r")
    if headline in f:
        break
    else:
        cache_nyt_file.write(headline + "\n")

# writing for loop
for x in range(10): 

    # calling NYT API
    base_url_nyt = "https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=section_name%3A%22New%20York%22&sort=newest&begin_date=20191108&end_date=20191208&page={}&api-key=IeOc9X1YnyZgg5W1JAujzDAKJaG8H1bR".format(x)

    r_nyt = requests.get(base_url_nyt) 
    d_nyt = r_nyt.json()

    cache_nyt = dir_path + '/' + "nyt_cache.json"
    if os.path.isfile(cache_nyt):
        cache_nyt_read = open(cache_nyt, "r")
        lines = cache_nyt_read.readlines()
        if len(lines) < 100:
            cache_nyt_file = open(cache_nyt, "a")
            for d in d_nyt["response"]["docs"]:
                headline = d["abstract"]
                duplicates(headline, cache_nyt_file)
            cache_nyt_file.close()

    else:
        # creating cache for NYT files
        cache_nyt_file = open(cache_nyt, "w")
        for d in d_nyt["response"]["docs"]:
            headline = d["abstract"]
            cache_nyt_file.write(headline + "\n")
        cache_nyt_file.close()


# reading cache dictionary contents
"""cache_file_nyt = open(cache_nyt, 'r')
cache_contents_nyt = cache_file_nyt.read()
cache_dict_nyt= json.loads(cache_contents_nyt)
cache_file_nyt.close()"""

