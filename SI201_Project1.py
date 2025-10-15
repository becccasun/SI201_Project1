# SI 201 Project 1
# Rebecca Sun, with help from ChatGPT
# 10/06/2025
# 18852123
# beccasun@umich.edu

import csv

with open('penguins.csv', newline="") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)

# Question 1: percent of 2007 penguins that are Adelie (species)
# Question 2: average body mass (g) of all Adelie penguins

def analyze_penguins(csv_path, out_path="penguin_results.txt"):
   # Q1
   adelie_2007 = 0
   total_2007 = 0
   # Q2
   adelie_mass_total = 0 
   adelie_mass_count = 0
   
   # Each row as dictionary
   with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            species = (row.get("species") or "").strip()
            island = (row.get("island") or "").strip()
            year = str(row.get("year") or "").strip()
            body_mass = (row.get("body_mass_g") or "").strip()

            # % of 2007 penguins that are Adelie
            if species and year and island:
                if year =="2007":
                    total_2007 += 1
                    if species == "Adelie":
                        adelie_2007 += 1


            # average body mass for all adelie penguins
            if species == "Adelie" and body_mass:
                try:
                    mass_value = float(body_mass)
                    adelie_mass_total += mass_value
                    adelie_mass_count += 1
                except ValueError:
                    pass
            
    # calculate results
    # Q1
        if total_2007 > 0:
            percent_adelie_2007 = (adelie_2007 / total_2007) * 100
        else:
            percent_adelie_2007 = 0.0

    # Q2
        if adelie_mass_count > 0:
            average_adelie_mass = adelie_mass_total / adelie_mass_count
        else:
            average_adelie_mass = 0.0


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
     

