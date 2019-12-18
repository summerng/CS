"""

sentiment.py

This file extracts the headlines from <headline database>, runs API calls for them on
<sentiment API>, and then stores the 

"""

import paralleldots
import sqlite3
paralleldots.set_api_key("W6l89LRnF8YE1eRBW1rD2yqzCgOKOWvyZcxpNSD9nLo")


def call_sentiment_api(database_filename, conn, cur):

    # Print opening message for this program action
    print(
    """
    ================================================================================
    = Collect text sentiment values for headlines/abstracts from Parallel Dots API =
    ================================================================================
    """
    )

    # Create the negative, neutral, and positive sentiment tables in the sentiment database
    cur.execute('CREATE TABLE IF NOT EXISTS "Negative Sentiment Per Headline and Abstract" ' + 
                    '(id INTEGER PRIMARY KEY, "Headline and Abstract" TEXT, "Negative Sentiment" REAL)')
    cur.execute('CREATE TABLE IF NOT EXISTS "Neutral Sentiment Per Headline and Abstract" ' + 
                    '(id INTEGER PRIMARY KEY, "Headline and Abstract" TEXT, "Neutral Sentiment" REAL)')
    cur.execute('CREATE TABLE IF NOT EXISTS "Positive Sentiment Per Headline and Abstract" ' + 
                    '(id INTEGER PRIMARY KEY, "Headline and Abstract" TEXT, "Positive Sentiment" REAL)')

    # Select the headlines
    cur.execute("SELECT Headlines.Headline, Abstracts.Abstract FROM Headlines INNER JOIN Abstracts ON Headlines.id" +
                " = Abstracts.id")
    call_list = []
    id_count = 0 ################################################

    for row in cur.fetchall():
        headline = row[0]
        abstract = row[1]
        headline_and_abstract = headline + " " + abstract

        # Should check other two tables too
        # Change headline to id
        cur.execute('SELECT "Headline and Abstract" FROM "Negative Sentiment Per Headline and Abstract" WHERE ' + 
                    '"Headline and Abstract" = ?', (headline_and_abstract,))

        # If this headline is not in the sentiment database, add it to the call list
        if cur.fetchone() == None:
            call_list.append(headline_and_abstract)

        # else:
        #     sent_cur.execute('SELECT Headline FROM "Predominant Sentiment Types" WHERE Headline = ?', (headline,))
        #     if sent_cur.fetchone() == None:
        #         add_sentiment_type_to_existing(headline)

        id_count += 1 ########################################################################3

        # Once the call_list reaches 20 new items, move on to calling API
        if len(call_list) == 20:
            break
    

    # Call API if there are any new items in call list
    if len(call_list) > 0:

        # Call Paralleldots API on list of new items
        english = "en"
        response = paralleldots.batch_sentiment(call_list, english)
        sentiment_list = response["sentiment"]

        # Loop through each headline and add the headline and three sentiment values
        # to sentiment database
        for ix in range(len(sentiment_list)):
            headline_and_abstract = call_list[ix]
            neg_sent = sentiment_list[ix]["negative"]
            neut_sent = sentiment_list[ix]["neutral"]
            pos_sent = sentiment_list[ix]["positive"]

            id_val = id_count - len(sentiment_list) + 1 + ix ##############################################################

            cur.execute('INSERT INTO "Negative Sentiment Per Headline and Abstract" VALUES (?,?,?)', (id_val, headline_and_abstract, neg_sent))
            cur.execute('INSERT INTO "Neutral Sentiment Per Headline and Abstract" VALUES (?,?,?)', (id_val, headline_and_abstract, neut_sent))
            cur.execute('INSERT INTO "Positive Sentiment Per Headline and Abstract" VALUES (?,?,?)', (id_val, headline_and_abstract, pos_sent))

    conn.commit()

    print("\tAdded {} rows to the sentiment tables in \"{}\".".format(len(call_list), database_filename))
    cur.execute('SELECT "Headline and Abstract" FROM "Negative Sentiment Per Headline and Abstract"')
    print("\tThere are now {} total rows for each sentiment table in \"{}\".".format(len(cur.fetchall()), database_filename))

    

    get_more = input("\tWould you like to calculate 2o more values? Yes or No: ")

    if get_more == "Yes":
        call_sentiment_api(database_filename, conn, cur)