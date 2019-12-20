import requests
import json
import os
import sqlite3
import paralleldots


def get_headlines_and_abstracts(database_filename, conn, cur):

    # Print opening message for this program action
    print(
    """
    ================================================================================
    =         Collect 20 headlines and abstracts from New York Times API           =
    ================================================================================
    """
    )

    cur.execute("CREATE TABLE IF NOT EXISTS Headlines (id INTEGER PRIMARY KEY, Headline TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS Abstracts (id INTEGER PRIMARY KEY, Abstract TEXT)")
 
    headline_list = []
    abstract_list = []
    tot = 0 

    # writing for loop - it is range 11 instead of 10 because there are repeat headlines that we shouldn't collect twice
    for x in range(11): 
        

        # calling NYT API
        base_url_nyt = "https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=section_name%3A%22New%20York%22&sort=newest&begin_date=20191108&end_date=20191208&page={}&api-key=IeOc9X1YnyZgg5W1JAujzDAKJaG8H1bR".format(x)

        r_nyt = requests.get(base_url_nyt) 
        d_nyt = r_nyt.json()

        if tot < 20: 
            try:
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

            except:
                print("\tThe API sent back a call limit exceeded message. Please wait a moment and try again or restart the program.")
                return
        else:
            break

    conn.commit()
    
    print("\tAdded {} rows to all three tables in \"{}\".".format(tot, database_filename))
    cur.execute('SELECT Headline FROM Headlines')
    print("\tThere are now {} total rows for each table in \"{}\".".format(len(cur.fetchall()), database_filename))

    get_more = input("\tWould you like to collect 20 more headlines and abstracts? Yes or No: ")

    if get_more == "Yes":
        get_headlines_and_abstracts(database_filename, conn, cur)