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
# testing branch

base_url_nyt = "https://api.nytimes.com/svc/search/v2/articlesearch.json?facet_fields=section_name&facet_filter=true&fq=NYRegion&page=1&sort=newest&api-key=SvJpgvBj8k1I1TILI9oOGjA01uR2JQkc"
r_nyt = requests.get(base_url_nyt) 
d_nyt = r_nyt.json()

# creating cache dictionary for NYT api
cache_nyt = dir_path + '/' + "nyt_cache.json"
with open(cache_nyt, "w") as json_file:
    json.dump(d_nyt, json_file)

# reading cache dictionary contents
cache_file_nyt = open(cache_nyt, 'r')
cache_contents_nyt = cache_file_nyt.read()
cache_dict_nyt= json.loads(cache_contents_nyt)
cache_file_nyt.close()

