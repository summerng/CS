import os

def ask_for_csv_filename():
    # Get the filename of the headline/abstract database via user input
    csv_filename = input("\tPlease enter a name for the csv file you would like to use to compose the visualization: ")
    if not csv_filename.endswith(".csv"):
        csv_filename += ".csv"
    return csv_filename

def file_reader(filename):

    # hover to show headline + abstract
    list_1 = []
    list_2 = []
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path, "r")
    lines = f.readlines()
    for line in lines[1:]:
        line = line.split(",")
        list_1.append(int(line[0]))
        list_2.append(float(line[1].strip()))

    return (list_1, list_2)