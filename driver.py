# Driver.py

import csv
import json
import os
import paralleldots
import requests
import sqlite3

from sentiment import call_sentiment_api
from wellbeing_calculator import calculate_wellbeing_scores 
from headlines_abstracts import get_headlines_and_abstracts
from quality_of_life import get_quality_of_life_for_NY
from bar_chart import compose_bar_chart
from scatterplot import scatterplot
from piechart import piechart
from file_reader import file_reader
from file_reader import ask_for_csv_filename

paralleldots.set_api_key("W6l89LRnF8YE1eRBW1rD2yqzCgOKOWvyZcxpNSD9nLo")


def print_opening():
    print(
    """
    = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
    
        Welcome to "Accuracy of New York Headlines and Abstracts Against Quality of Life Measure"
    
    Description:
            * Firstly, This program collects news headlines or abstracts  
              from the New York Times API and stores them in a database.  
            * Secondly, the program can then run each of the headlines 
              and abstracts through Parallel Dots, a text sentiment 
              analyzer API, to get the positive, neutral, and negative
              text sentiment scores for a given headline and abstract.  
            * Thirdly, the program uses these scores to calculate an 
              overall sentiment score for each headline and abstract pair
              and stores this data in a csv file. 
            * Fourthly, the program calls the Teleport API to retrieve 
              the overall quality of life metric for the New York
              region in order to use it in the scatter plot visualization.
            * Fifthly, the program allows for the composition of a 
              scatterplot, bar chart, and pie chart to represent the
              calculated data in the csv file.
    """
    )


def print_closing():
    print(
    """
    Thank you for using Accuracy of New York Headlines Against Quality of Life Measure!!!

    Exiting...
    """
    )


def ask_for_database_filename():
    # Get the filename of the headline/abstract database via user input
    database_filename = input("\tPlease enter a name for a new or existing database you would like to use: ")

    try:
        # Connect to the headline/abstract database
        conn = sqlite3.connect(database_filename)
        cur = conn.cursor()
        print("\tUsing \"{}\"".format(database_filename))
        return (database_filename, conn, cur)
    except:
        print("Error with opening database. Trying again.\n")
        return (database_filename)


def handle_input(database_filename, conn, cur):
    user_input = input(
    """
    Please enter a number (1-8) to perform an action:
    Please perform actions 1, 2, and 3 in order before anything else.

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
        scatterplot()
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