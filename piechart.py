import os
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import csv


def piechart(database_filename, conn, cur):
    neg = 0
    neut = 0
    pos = 0
    cur.execute('SELECT Headlines.id, Headlines.Headline, Abstracts.Abstract, ' + \
               '"Negative Sentiment Per Headline and Abstract"."Negative Sentiment", ' + \
               '"Neutral Sentiment Per Headline and Abstract"."Neutral Sentiment", ' + \
               '"Positive Sentiment Per Headline and Abstract"."Positive Sentiment" ' + \
               'FROM Headlines INNER JOIN Abstracts ON Headlines.id = Abstracts.id ' + \
               'INNER JOIN "Negative Sentiment Per Headline and Abstract" ON ' + \
               'Headlines.id = "Negative Sentiment Per Headline and Abstract".id ' + \
               'INNER JOIN "Neutral Sentiment Per Headline and Abstract" ON ' + \
               'Headlines.id = "Neutral Sentiment Per Headline and Abstract".id ' + \
               'INNER JOIN "Positive Sentiment Per Headline and Abstract" ON ' + \
               'Headlines.id = "Positive Sentiment Per Headline and Abstract".id')

    
    for row in cur.fetchall():
        row = row[3:]
        if row[0] > row[1] and row [0] > row[2]:
            neg += 1
        elif row[1] > row[0] and row[1] > row[2]:
            neut += 1
        else:
            pos += 1
    labels = ["Negative", "Neutral", "Positive"]
    values = [neg, neut, pos]
    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig_pie.update_layout(
        title="Distribution of Negative, Neutral, and Positive Headlines/Abstracts",
    )
    print(
    """
    ================================================================================
                               = Creating scatterplot =
    ================================================================================
    """
    )
    fig_pie.show()


