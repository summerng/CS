# Driver.py

import csv
import json
import os
import paralleldots
import requests
import sqlite3

#from sentiment import call_sentiment_api
from wellbeing_calculator import calculate_wellbeing_scores 
from headlines_abstracts import get_headlines_and_abstracts
from quality_of_life import get_quality_of_life_for_NY
from scatterplot import scatterplot
from piechart import piechart

paralleldots.set_api_key("W6l89LRnF8YE1eRBW1rD2yqzCgOKOWvyZcxpNSD9nLo")


def print_opening():
    print(
    """
    = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    
                Welcome to "Accuracy of New York Headlines Against Wellbeing Measure"
    
    Description:
            Firstly, This program collects news headlines or abstracts  
            from the New York Times API and stores them in a database.  
            Secondly, the program can then run each of the headlines or
            abstracts through a text sentiment analyzer API to get the 
            positive, neutral, and negative sentiment scores for a given
            headline or abstract.  Thirdly, the program uses these scores
            to calculate a predicted wellbeing score for each headline
            or abstract.  Fourthly, the program calls the ...
    """
    )


def ask_for_database_filename():
    # Get the filename of the headline/abstract database via user input
    database_filename = input("Please enter a name for a new or existing database you would like to use: ")

    try:
        # Connect to the headline/abstract database
        conn = sqlite3.connect(database_filename)
        cur = conn.cursor()
        print("")
        return (database_filename, conn, cur)
    except:
        print("Error with opening database. Trying again.\n")
        return (database_filename)


def print_closing():
    print(
    """
    Thank you for using <Program name>!!!

    Exiting...
    """
    )

def handle_input(database_filename, conn, cur):
    user_input = input(
    """
    Please enter a number (1-5) to perform an action:
        API
            (1) Collect 20 headlines and abstracts from New York Times API
            (2) Collect 20 sets of text sentiment values for headlines and abstracts from Parallel Dots API
        CALCULATE
            (3) Calculate wellbeing scores for headlines/abstracts
        VISUALIZE
            (4) Compose scatter plot
            (5) Compose bar chart
            (6) Compose pie chart
            (7) Compose some other graph
        
        OTHER
            (8) Quit
    User input: """)

    if user_input   == "1":
        get_headlines_and_abstracts(database_filename, conn, cur)
    elif user_input == "2":
        call_sentiment_api(database_filename, conn, cur)
    elif user_input == "3":
        calculate_wellbeing_scores(database_filename, conn, cur)
    elif user_input == "4":
        scatterplot("quality_of_life.csv")
    elif user_input == "5":
        compose_bar_chart()
    elif user_input == "6":
        piechart(database_filename, conn, cur)
    elif user_input == "7":
        """Implement"""
    elif user_input == "8":
        """Implement"""
        return False
    # else
    return True


# The main function where the program starts out in
def main():
    print_opening()

    database_info = ask_for_database_filename()

    # Prompt for database filename until valid input
    while len(database_info) == 1:
        database_info = ask_for_database_filename()
    
    database_filename, conn, cur = database_info

    while (handle_input(database_filename, conn, cur)): 
        """ Loop until user quits """

    conn.close()
    print_closing()


# If python file is not imported, start with main function
if __name__ == '__main__':
    main()