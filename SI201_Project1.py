# SI 201 Project 1
# Rebecca Sun, working wit Junjin Tan, Anu Narayan
# 10/06/2025
# 18852123
# beccasun@umich.edu

import csv

with open('penguins.csv', newline="") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)

# number of adelie penguins
# number of female penguins

def analyze_penguins(csv_path: str, out_path: str = "penguin_results.txt") -> None:
    #Read penguin.csv, analyze data, and writes a report to out_path
    total_adelie = 0
    total_female = 0

    year_sum = 0
    year_count = 0

    with open(csv_path, newline ="") as csvfile:
        reader = csv.reader(csvfile)
        # % of adelie penguins
