# SI 201 Project 1
# Rebecca Sun, with help from ChatGPT
# 10/06/2025
# 18852123
# beccasun@umich.edu

import csv

# (Optional) quick preview: show first 5 rows so the console isn't flooded
with open('penguins.csv', newline="") as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        print(row)
        if i >= 4:
            break

# Question 1: percent of 2007 penguins that are Adelie (species)
# Question 2: average body mass (g) of all Adelie penguins

def analyze_penguins(csv_path, out_path="penguin_results.txt"):
    # Q1 counters
    adelie_2007 = 0
    total_2007 = 0

    # Q2 accumulators
    adelie_mass_total = 0.0
    adelie_mass_count = 0

    # Read each row as a dictionary
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            species = (row.get("species") or "").strip()
            island = (row.get("island") or "").strip()
            year = str(row.get("year") or "").strip()
            body_mass = (row.get("body_mass_g") or "").strip()

            # ---- Q1: % of 2007 samples that are Adelie ----
            # Only count rows where species, year, and island are present (3 columns)
            if species and year and island:
                if year == "2007":
                    total_2007 += 1
                    if species == "Adelie":
                        adelie_2007 += 1

            # ---- Q2: average body mass for Adelie (species) ----
            # Require species + island + body_mass_g; ignore non-numeric masses
            if species and island and body_mass and species == "Adelie":
                try:
                    mass_value = float(body_mass)
                    adelie_mass_total += mass_value
                    adelie_mass_count += 1
                except ValueError:
                    pass  # skip rows where body_mass_g isn't a number

    # ---- Calculate results (OUTSIDE the loop) ----
    # Q1
    if total_2007 > 0:
        percent_adelie_2007 = (adelie_2007 / total_2007) * 100
    else:
        percent_adelie_2007 = 0.0

    # Q2
    if adelie_mass_count > 0:
        average_adelie_mass = adelie_mass_total / adelie_mass_count
    else:
        average_adelie_mass = 0.0  # or use None/"n/a" if you prefer

    # ---- Write report
    report_lines = [
        f"File: {csv_path}",
        "---------------------------",
        "Q1) What percent of 2007 samples are Adelie (species)?",
        f"  Total rows in 2007:                 {total_2007}",
        f"  Adelie (species) rows in 2007:      {adelie_2007}",
        f"  % of 2007 that is Adelie (species): {percent_adelie_2007:.2f}%",
        "",
        "Q2) What is the average body mass of Adelie (species)?",
        f"  Average body mass (grams):          {average_adelie_mass:.2f} grams",
    ]
    with open(out_path, "w", encoding="utf-8") as out:
        out.write("\n".join(report_lines))

    # Also print to the screen so you see the answers
    print("\n".join(report_lines))

# Run the analysis
if __name__ == "__main__":
    analyze_penguins("penguins.csv")
