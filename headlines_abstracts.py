import requests
import json
import os
import sqlite3
import paralleldots


# PART 2: Calling New York Times (NYT) API

"""
NYT API only returns 10 results at a time, so we have to
call it 10 times for a total of 100 results.
SIDENOTE!!!: i'm a bit unsure by the instructions if we need to 
run our code 10 times to get the data or if using a for loop is fine?
"""
# create empty list, check to see if headline is in list, keep adding until 20 and then break

def get_headlines_and_abstracts(database_filename, conn, cur):
    #conn = sqlite3.connect("/Users/BinhNguyenAn/Desktop/SI_206/CS/headlines.db")

    # creating database
    #ur = conn.cursor()

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

    
    print("Added {} rows to all three tables in \"{}\".".format(tot, database_filename))
    cur.execute('SELECT Headline FROM Headlines')
    print("There are now {} total rows for each table in \"{}\".".format(len(cur.fetchall()), database_filename))

    get_more = input("Would you like to collect 2o more headlines and abstracts? Yes or No: ")

    if get_more == "Yes":
        get_headlines_and_abstracts(database_filename, conn, cur)