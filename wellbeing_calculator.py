"""

wellbeing_calculator.py

This file calculates the wellbeing score for the headlines and abstracts
in the sentiments database.

"""

import os
import csv

def calculate_wellbeing_scores(database_filename, conn, cur):
    # Print opening message for this program action
    print(
    """
    ======================================================
    = Calculate wellbeing scores for headlines/abstracts =
    ======================================================
    """
    )

    # Using JOIN
    cur.execute('SELECT Headlines.id, Headlines.Headline, Abstracts.Abstract, ' + \
               '"Negative Sentiment Per Headline and Abstract"."Negative Sentiment", ' +\
               '"Neutral Sentiment Per Headline and Abstract"."Neutral Sentiment", ' + \
               '"Positive Sentiment Per Headline and Abstract"."Positive Sentiment" ' + \
               'FROM Headlines INNER JOIN Abstracts ON Headlines.id = Abstracts.id ' + \
               'INNER JOIN "Negative Sentiment Per Headline and Abstract" ON ' + \
               'Headlines.id = "Negative Sentiment Per Headline and Abstract".id ' + \
               'INNER JOIN "Neutral Sentiment Per Headline and Abstract" ON ' + \
               'Headlines.id = "Neutral Sentiment Per Headline and Abstract".id ' + \
               'INNER JOIN "Positive Sentiment Per Headline and Abstract" ON ' + \
               'Headlines.id = "Positive Sentiment Per Headline and Abstract".id')

    data_list = []
    for row in cur.fetchall():
        id_ = row[0]

        neg_sent  = row[3]
        neut_sent = row[4]
        pos_sent  = row[5]

        wellbeing = round(100 * pos_sent + 50 * neut_sent + 0 * neg_sent, 2)

        data_list.append((id_, wellbeing))

    write_to_file(data_list)


def write_to_file(data_list):

    filename = input("\tEnter the csv filename where you would like to save this data: ")
    if not filename.endswith(".csv"):
        filename += ".csv"

    full_path = os.path.join(os.path.dirname(__file__), filename)

    # Added encoding="utf8" to make it work on my computer
    with open(full_path, 'w', newline='', encoding="utf8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["id", "quality of life metric"])
        csvwriter.writerows(data_list)

    print("\tWrote calculated data to \"{}\"".format(filename))
  