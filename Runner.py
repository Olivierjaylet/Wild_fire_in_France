# riche-pro@hotmail.fr
# 20/10 à 20h

# command line to execute in the terminal : "runner.py [year] [department]" or "python runner.py [year] [department]"
# if no department chosen, the default value is '00' which selects all departments
# example : "runner.py 2013 13" ; for Bouches-du-Rhône in 2013
# or : "runner.py 2013" ; for all departments in 2013
#
#

from PrometheusLib import *
import pandas as pd
import sys
from tabulate import tabulate


year = int(sys.argv[1])
try : # if department given in input
    sys.argv[2]
    department = sys.argv[2]
except : # If department doesnt exist, we select all
    department = '00'

csv_file ="liste_incendies_ du_12_08_2022.csv"


# run all functions from the library
dataframe = dataclean(csv_file)
nombre_fires = nb_fires(dataframe, department, year)
burnt = burnt_area(dataframe, department, year)
department, year, mean, Q1, Q3 = des(dataframe,department, year)
plot_department_timeseries(dataframe, department)
plot_pie_chart(dataframe, year)


# Define datas as a list of lists (each inner list represents a row)
data = [
    [department, year, nombre_fires, burnt, mean, Q1, Q3],
]
# Specify the headers for the table
headers = ["Department", "Year", "Number of fires", "Burnt area", "mean", "Q1", "Q3"]

# Create the table row
table = tabulate(data, headers=headers, tablefmt="grid")

# Print the table row
print(table)