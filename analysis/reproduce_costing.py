#!/usr/bin/env python3
"""Reproduce headline costing figures and generate the cost chart.

Run from any location with:
    python analysis/reproduce_costing.py
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COST_FILE = ROOT / "data" / "national-cost-estimate.csv"
FUNDING_FILE = ROOT / "data" / "funding-scenarios.csv"
CHART_FILE = ROOT / "visuals" / "cost-breakdown.png"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    costs = read_csv(COST_FILE)
    scenarios = read_csv(FUNDING_FILE)

    total = sum(int(row["annual_cost_gbp"]) for row in costs)
    print(f"Central annual cost estimate: £{total / 1_000_000:,.2f} million")
    print(f"Rounded policy estimate: £{total / 1_000_000:,.0f} million")

    for row in scenarios:
        revenue = int(row["revenue_base_gbp"])
        rate = float(row["allocation_rate"])
        recorded = int(row["calculated_allocation_gbp"])
        calculated = round(revenue * rate)
        if calculated != recorded:
            raise ValueError(f"Funding calculation mismatch for {row['scenario']}")
        print(f"{row['scenario']}: £{calculated / 1_000_000:,.2f} million")

    try:
        import matplotlib.pyplot as plt
        from matplotlib.ticker import FuncFormatter
    except ImportError as exc:
        raise SystemExit(
            "Chart generation requires matplotlib. Install it with "
            "'python -m pip install matplotlib'."
        ) from exc

    labels = [row["cost_item"] for row in costs]
    values = [int(row["annual_cost_gbp"]) / 1_000_000 for row in costs]

    fig, ax = plt.subplots(figsize=(10, 5.8))
    bars = ax.barh(labels[::-1], values[::-1], color="#176B87")
    ax.set_title("Climate Civic Festival: central annual cost estimate", loc="left", weight="bold")
    ax.set_xlabel("£ million per year")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"£{value:g}m"))
    ax.grid(axis="x", alpha=0.22)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)

    for bar, value in zip(bars, values[::-1]):
        ax.text(
            bar.get_width() + 0.35,
            bar.get_y() + bar.get_height() / 2,
            f"£{value:.2f}m",
            va="center",
            fontsize=9,
        )

    ax.text(
        0,
        -0.19,
        f"Total: £{total / 1_000_000:.2f}m, reported in the proposal as approximately £65m.",
        transform=ax.transAxes,
        fontsize=9,
        color="#444444",
    )
    fig.subplots_adjust(left=0.40, right=0.96, top=0.88, bottom=0.20)
    CHART_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(CHART_FILE, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Chart written to: {CHART_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
