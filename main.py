import requests
import json
import os
import sqlite3
import paralleldots

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

# writing for loop - it is range 11 instead of 10 because there are repeat headlines that we shouldn't collect twice
for x in range(11): 

    # calling NYT API
    base_url_nyt = "https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=section_name%3A%22New%20York%22&sort=newest&begin_date=20191108&end_date=20191208&page={}&api-key=IeOc9X1YnyZgg5W1JAujzDAKJaG8H1bR".format(x)

    cache_nyt = dir_path + '/' + "nyt_cache.json"

    # checks if cache exists
    if os.path.isfile(cache_nyt):

        # checks if file has 100 lines - if not, keep adding
        cache_nyt_read = open(cache_nyt, "r")
        lines = cache_nyt_read.readlines()
        if len(lines) < 100:
            r_nyt = requests.get(base_url_nyt) 
            d_nyt = r_nyt.json()
            # appending more lines to file
            cache_nyt_file = open(cache_nyt, "a")
            for d in d_nyt["response"]["docs"]:
                headline = d["headline"]["main"]
                if headline not in lines:
                    cache_nyt_file.write(headline)
                    cache_nyt_file.write("\n")
            cache_nyt_read.close()
            cache_nyt_file.close()

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


""" ignore this
# reading cache dictionary contents
cache_file_nyt = open(cache_nyt, 'r')
cache_contents_nyt = cache_file_nyt.read()
cache_dict_nyt= json.loads(cache_contents_nyt)
cache_file_nyt.close()"""

"""# PART 3: Calling the Parallel Dots (word sentiment analyzer) API
paralleldots.set_api_key("RI2jA3tZ4QUsNnLzdytEQ0cn9GSEkMgrGkXzgg1P8Hk")

cache_sentiment = dir_path + '/' + "sentiment.json"
lang_code = "en"
sentiment = paralleldots.batch_sentiment(lines, lang_code)  #reminder that lines was a variable defined above that is just a list of all of the headlines

# writing cache file
with open(cache_sentiment, "w") as json_file:
    json.dump(sentiment, json_file)
json_file.close()"""

# PART 4: Creating the Headlines database

# CHANGE THIS TO YOUR OWN DIRECTORY!!!!
conn = sqlite3.connect("/Users/BinhNguyenAn/Desktop/SI_206/CS/headlines.db")

# creating database
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS Headlines")
cur.execute("CREATE TABLE IF NOT EXISTS Headlines (Headline TEXT)")
for headline in lines: #reminder that lines was a variable defined above that is just a list of all of the headlines
    cur.execute("INSERT INTO Headlines (Headline) VALUES (?)", [headline])
conn.commit()
conn.close()


