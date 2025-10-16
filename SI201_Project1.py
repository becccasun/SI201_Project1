# SI 201 Project 1
# Rebecca Sun, with help from ChatGPT with debugging and code completion after attempting it myself first. It also helped with formatting the report.
# 10/06/2025
# 18852123
# beccasun@umich.edu

import csv
import unittest

# Analysis code

def analyze_penguins(csv_path, out_path="penguin_results.txt"):
    # Q1 counters
    adelie_2007 = 0
    total_2007 = 0

    # Q2 accumulators
    adelie_mass_total = 0.0
    adelie_mass_count = 0

    # Read each row as dictionary
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
        average_adelie_mass = 0.0

    # Write report
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

    # Also print to the screen
    print("\n".join(report_lines))


# Helper functions for tests 


def calc_percent_adelie_2007(rows):
    """
    Percent of 2007 samples that are Adelie (species), requiring species+year+island.
    Returns (percent_float, adelie_2007_count, total_2007_count).
    """
    adelie_2007 = 0
    total_2007 = 0
    for r in rows:
        species = (r.get("species") or "").strip()
        island  = (r.get("island")  or "").strip()
        year    = str(r.get("year") or "").strip()
        if species and island and year:
            if year == "2007":
                total_2007 += 1
                if species == "Adelie":
                    adelie_2007 += 1
    pct = (adelie_2007 / total_2007 * 100) if total_2007 else 0.0
    return pct, adelie_2007, total_2007


def calc_avg_mass_adelie(rows):
    """
    Average body mass (g) of Adelie (species), requiring species+island+body_mass_g.
    Skips NA/blank/non-numeric masses. Returns 0.0 if no valid rows.
    """
    total = 0.0
    count = 0
    for r in rows:
        species = (r.get("species") or "").strip()
        island  = (r.get("island")  or "").strip()
        mass_s  = r.get("body_mass_g")
        if species == "Adelie" and island:
            if mass_s is None:
                continue
            mass_s = str(mass_s).strip()
            if mass_s == "" or mass_s.upper() == "NA":
                continue
            try:
                total += float(mass_s)
                count += 1
            except ValueError:
                continue
    return (total / count) if count else 0.0


# Unit tests

class TestPenguinCalcs(unittest.TestCase):

    # ---------- calc_percent_adelie_2007 (4 tests) ----------

    # Usual 1: typical mix in 2007 (2 Adelie of 4 valid 2007 rows -> 50%)
    def test_percent_2007_usual_mixed(self):
        rows = [
            {"species":"Adelie","island":"Biscoe","year":"2007"},
            {"species":"Adelie","island":"Torgersen","year":"2007"},
            {"species":"Gentoo","island":"Dream","year":"2007"},
            {"species":"Chinstrap","island":"Biscoe","year":"2007"},
            # Incomplete rows should be ignored:
            {"species":"Adelie","island":"", "year":"2007"},
            {"species":"",       "island":"Adelie","year":"2007"},
        ]
        pct, a2007, total2007 = calc_percent_adelie_2007(rows)
        self.assertEqual(total2007, 4)
        self.assertEqual(a2007, 2)
        self.assertAlmostEqual(pct, 50.0, places=2)

    # Usual 2: all 2007 rows are Adelie (100%)
    def test_percent_2007_usual_all_adelie(self):
        rows = [
            {"species":"Adelie","island":"Biscoe","year":"2007"},
            {"species":"Adelie","island":"Dream","year":"2007"},
            {"species":"Adelie","island":"Torgersen","year":"2007"},
        ]
        pct, a2007, total2007 = calc_percent_adelie_2007(rows)
        self.assertEqual(total2007, 3)
        self.assertEqual(a2007, 3)
        self.assertAlmostEqual(pct, 100.0, places=2)

    # Edge 1: no 2007 rows at all -> percent 0, counts 0
    def test_percent_2007_edge_no_rows(self):
        rows = [
            {"species":"Adelie","island":"Biscoe","year":"2008"},
            {"species":"Gentoo","island":"Dream","year":"2009"},
        ]
        pct, a2007, total2007 = calc_percent_adelie_2007(rows)
        self.assertEqual(total2007, 0)
        self.assertEqual(a2007, 0)
        self.assertEqual(pct, 0.0)

    # Edge 2: only incomplete 2007 rows (missing species/island) -> totals stay 0
    def test_percent_2007_edge_incomplete_rows(self):
        rows = [
            {"species":"",       "island":"Biscoe", "year":"2007"},
            {"species":"Adelie","island":"",       "year":"2007"},
            {"species":"",       "island":"",      "year":"2007"},
        ]
        pct, a2007, total2007 = calc_percent_adelie_2007(rows)
        self.assertEqual(total2007, 0)
        self.assertEqual(a2007, 0)
        self.assertEqual(pct, 0.0)

    # ---------- calc_avg_mass_adelie (4 tests) ----------

    # Usual 1: average of valid Adelie masses (3400, 3800, 3200, 3300 -> 3425.0)
    def test_avg_mass_adelie_usual_full(self):
        rows = [
            {"species":"Adelie","island":"Biscoe","body_mass_g":"3400"},
            {"species":"Adelie","island":"Torgersen","body_mass_g":"3800"},
            {"species":"Adelie","island":"Biscoe","body_mass_g":"3200"},
            {"species":"Adelie","island":"Dream","body_mass_g":"3300"},
        ]
        avg = calc_avg_mass_adelie(rows)
        self.assertAlmostEqual(avg, 3425.0, places=2)

    # Usual 2: subset average (two rows -> (3400+3800)/2 = 3600)
    def test_avg_mass_adelie_usual_subset(self):
        rows = [
            {"species":"Adelie","island":"Biscoe","body_mass_g":"3400"},
            {"species":"Adelie","island":"Torgersen","body_mass_g":"3800"},
        ]
        avg = calc_avg_mass_adelie(rows)
        self.assertAlmostEqual(avg, 3600.0, places=2)

    # Edge 1: missing/NA/non-numeric masses are skipped (avg unchanged)
    def test_avg_mass_adelie_edge_skips_bad(self):
        rows = [
            {"species":"Adelie","island":"Biscoe","body_mass_g":"3400"},
            {"species":"Adelie","island":"Torgersen","body_mass_g":"NA"},
            {"species":"Adelie","island":"Dream","body_mass_g":"  "},
            {"species":"Adelie","island":"Biscoe","body_mass_g":"not_a_number"},
            {"species":"Adelie","island":"Dream","body_mass_g":"3800"},
        ]
        avg = calc_avg_mass_adelie(rows)
        self.assertAlmostEqual(avg, 3600.0, places=2)

    # Edge 2: no valid Adelie rows -> 0.0
    def test_avg_mass_adelie_edge_no_valid_rows(self):
        rows = [
            {"species":"Gentoo","island":"Biscoe","body_mass_g":"5000"},
            {"species":"Chinstrap","island":"Dream","body_mass_g":"4000"},
            {"species":"Adelie","island":"", "body_mass_g":"3700"},  # missing island -> ignore
            {"species":"Adelie","island":"Biscoe","body_mass_g":"NA"},  # NA -> ignore
        ]
        avg = calc_avg_mass_adelie(rows)
        self.assertEqual(avg, 0.0)


# Main: run tests first, then preview & analysis
if __name__ == "__main__":
    # Run unit tests (doesn't exit so analysis still runs)
    unittest.main(verbosity=2, exit=False)

    # Preview first 5 rows (guarded so it doesn't run during imports)
    try:
        with open('penguins.csv', newline="") as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                print(row)
                if i >= 4:
                    break
    except FileNotFoundError:
        print("penguins.csv not found for preview; continuing to analysis.")

    # Run the full analysis
    analyze_penguins("penguins.csv")
