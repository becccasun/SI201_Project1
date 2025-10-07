# SI 201 Project 1
# Rebecca Sun, working with Junjin Tan
# 10/06/2025
# 18852123
# beccasun@umich.edu

import csv

with open('penguins.csv', newline="") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)

# number of penguins of adelie
# number of penguins sampled in 2007

def analyze_penguins(csv_path, out_path="penguin_results.txt"):
    adelie_island_all = 0     # rows where island == "Adelie" (any year)
    rows_2007 = 0             # rows where year == "2007" (any island)
    adelie_island_2007 = 0    # rows where island == "Adelie" AND year == "2007"

    # Read each row as a dictionary
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            island = (row.get("island") or "").strip()
            year = str(row.get("year") or "").strip()

            # Count Adelie island overall
            if island == "Adelie":
                adelie_island_all += 1

            # Count all rows from 2007
            if year == "2007":
                rows_2007 += 1
                # Of those, how many are from Adelie island?
                if island == "Adelie":
                    adelie_island_2007 += 1

    # Avoid divide-by-zero
    if rows_2007 > 0:
        pct_adelie_island_of_2007 = (adelie_island_2007 / rows_2007) * 100
    else:
        pct_adelie_island_of_2007 = 0.0

    # Write report
    report_lines = [
        f"File: {csv_path}",
        "---------------------------",
        f"Adelie island (all years):     {adelie_island_all}",
        f"Total rows in 2007:            {rows_2007}",
        f"Adelie island rows in 2007:    {adelie_island_2007}",
        f"% of 2007 from Adelie island:  {pct_adelie_island_of_2007:.2f}%",
    ]
    with open(out_path, "w", encoding="utf-8") as out:
        out.write("\n".join(report_lines))

    # print on screen
    print("\n".join(report_lines))

# Run it
if __name__ == "__main__":
    analyze_penguins("penguins.csv")
     

