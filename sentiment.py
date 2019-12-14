"""

sentiment.py

This file extracts the headlines from <headline database>, runs API calls for them on
<sentiment API>, and then stores the 




"""

import paralleldots
import sqlite3

paralleldots.set_api_key("W6l89LRnF8YE1eRBW1rD2yqzCgOKOWvyZcxpNSD9nLo")

############################################################################################################3
# Connect to headlines database
head_conn = sqlite3.connect("headlines.db")
head_cur = head_conn.cursor()

# Connect to sentiment database
sent_conn = sqlite3.connect("sentiments_test")
sent_cur = sent_conn.cursor()

sent_cur.execute('CREATE TABLE IF NOT EXISTS "Sentiment Values" (Headline TEXT PRIMARY KEY, ' +
                 '"Negative Sentiment" REAL, "Neutral Sentiment" REAL, "Positive Sentiment" REAL)')
sent_cur.execute('CREATE TABLE IF NOT EXISTS "Predominant Sentiment Types" (Headline TEXT PRIMARY KEY, ' +
                 '"Predominant Sentiment Type" TEXT)')
# sent_cur.execute("CREATE TABLE IF NOT EXISTS Negative_Sentiment")
# sent_cur.execute("CREATE TABLE IF NOT EXISTS Neutral_Sentiment")
# sent_cur.execute("CREATE TABLE IF NOT EXISTS Positive_Sentiment")


english = "en"


def call_api():

    head_cur.execute("SELECT Headline FROM Headlines")
    call_list = []
    count = 0

    for row in head_cur:
        headline = row[0].strip()  # Should probably strip anyway beforehand

        sent_cur.execute('SELECT Headline FROM "Sentiment Values" WHERE Headline = ?', (headline,))

        if sent_cur.fetchone() == None:
            call_list.append(headline)
            count += 1
        else:
            sent_cur.execute('SELECT Headline FROM "Predominant Sentiment Types" WHERE Headline = ?', (headline,))
            if sent_cur.fetchone() == None:
                add_sentiment_type_to_existing(headline)

        if count == 20:
            break
    
    # Call API
    if len(call_list) > 0:

        response = paralleldots.batch_sentiment(call_list, english)

        sentiment_list = response["sentiment"]

        for ix in range(len(sentiment_list)):
            headline = call_list[ix].strip('"')
            neg_sent = sentiment_list[ix]["negative"]
            neut_sent = sentiment_list[ix]["neutral"]
            pos_sent = sentiment_list[ix]["positive"]

            table_values = [headline, neg_sent, neut_sent, pos_sent]

            sentiment_values = [neg_sent, neut_sent, pos_sent]
            max_sentiment_value = max(sentiment_values)
            sentiment_type = "Positive"

            if max_sentiment_value == neg_sent: sentiment_type = "Negative"
            elif max_sentiment_value == neut_sent: sentiment_type = "Neutral"

            sent_cur.execute('INSERT INTO "Sentiment Values" VALUES (?,?,?,?)', table_values)
            sent_cur.execute('INSERT INTO "Predominant Sentiment Types" VALUES (?,?)', (headline, sentiment_type))


    get_more = input("Would you like to calculate 2o more values? Y or N")

    if get_more == "Y":
        call_api()


def add_sentiment_type_to_existing(headline):
    sent_cur.execute('SELECT "Negative Sentiment", "Neutral Sentiment", "Positive Sentiment" FROM "Sentiment Values" WHERE Headline = ?', (headline,))
    neg_sent, neut_sent, pos_sent = sent_cur.fetchone()

    table_values = [headline, neg_sent, neut_sent, pos_sent]

    sentiment_values = [neg_sent, neut_sent, pos_sent]
    max_sentiment_value = max(sentiment_values)
    sentiment_type = "Positive"

    if max_sentiment_value == neg_sent: sentiment_type = "Negative"
    elif max_sentiment_value == neut_sent: sentiment_type = "Neutral"

    sent_cur.execute('INSERT INTO "Predominant Sentiment Types" VALUES (?,?)', (headline, sentiment_type))



    
call_api()

sent_conn.commit()
head_conn.close()
sent_conn.close()




