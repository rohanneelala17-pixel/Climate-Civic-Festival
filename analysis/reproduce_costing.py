import csv
import os

import matplotlib.pyplot as plt


# Find the main project folder from the location of this script.
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cost_file = os.path.join(project_folder, "data", "national-cost-estimate.csv")
funding_file = os.path.join(project_folder, "data", "funding-scenarios.csv")
chart_file = os.path.join(project_folder, "visuals", "cost-breakdown.png")


# Read the annual cost estimates.
cost_labels = []
costs_in_millions = []
total_cost = 0

with open(cost_file, encoding="utf-8") as file:
    rows = csv.DictReader(file)

    for row in rows:
        cost = int(row["annual_cost_gbp"])
        cost_labels.append(row["cost_item"])
        costs_in_millions.append(cost / 1000000)
        total_cost = total_cost + cost

print("Central annual cost estimate: £" + format(total_cost / 1000000, ".2f") + " million")
print("Rounded policy estimate: £" + format(total_cost / 1000000, ".0f") + " million")


# Check the three UK ETS funding calculations.
with open(funding_file, encoding="utf-8") as file:
    rows = csv.DictReader(file)

    for row in rows:
        revenue = int(row["revenue_base_gbp"])
        rate = float(row["allocation_rate"])
        expected_result = int(row["calculated_allocation_gbp"])
        result = round(revenue * rate)

        if result != expected_result:
            raise ValueError("The funding calculation does not match the CSV file.")

        print(row["scenario"] + ": £" + format(result / 1000000, ".2f") + " million")


# Create a horizontal bar chart of the programme costs.
plt.figure(figsize=(10, 5.8))
bars = plt.barh(cost_labels, costs_in_millions, color="#176B87")
plt.gca().invert_yaxis()
plt.title("Climate Civic Festival: central annual cost estimate", loc="left", fontweight="bold")
plt.xlabel("£ million per year")
plt.grid(axis="x", alpha=0.22)
plt.gca().set_axisbelow(True)

for bar, value in zip(bars, costs_in_millions):
    plt.text(
        value + 0.35,
        bar.get_y() + bar.get_height() / 2,
        "£" + format(value, ".2f") + "m",
        va="center",
    )

plt.figtext(
    0.40,
    0.02,
    "Total: £" + format(total_cost / 1000000, ".2f") + "m, reported in the proposal as approximately £65m.",
    fontsize=9,
    color="#444444",
)
plt.subplots_adjust(left=0.40, right=0.96, top=0.88, bottom=0.20)
plt.savefig(chart_file, dpi=180, bbox_inches="tight", facecolor="white")
plt.close()

print("Chart saved to visuals/cost-breakdown.png")
