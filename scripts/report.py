"""
Print the key findings and regenerate the README chart.

Run from the repository root, after data_cleaning.py has produced
data/processed/crop_production_clean.csv:

    py scripts/report.py

Writes: docs/top_crops.png
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

CLEAN_FILE = Path("data/processed/crop_production_clean.csv")
CHART_FILE = Path("docs/top_crops.png")

TOP_N = 8

# Coconut is recorded in nuts, not tonnes, so it is not comparable with the
# tonnage crops. Including it makes one crop 92% of the dataset total and
# turns every ranking into a statement about units rather than farming.
EXCLUDED_FROM_RANKING = "Coconut"


def load_clean() -> pd.DataFrame:
    """Read the cleaned dataset, telling the user what to do if it is missing."""
    if not CLEAN_FILE.exists():
        raise FileNotFoundError(
            f"'{CLEAN_FILE}' not found. Run 'py scripts/data_cleaning.py' first."
        )
    return pd.read_csv(CLEAN_FILE)


def rankings(df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """Return (by total production, by yield per hectare), both descending."""
    by_production = df.groupby("crop")["production"].sum().sort_values(ascending=False)
    by_yield = (
        df.groupby("crop")
        .agg(total_production=("production", "sum"), total_area=("area", "sum"))
        .assign(yield_per_hectare=lambda d: d["total_production"] / d["total_area"])
        ["yield_per_hectare"]
        .sort_values(ascending=False)
    )
    return by_production, by_yield


def findings(df: pd.DataFrame) -> None:
    """Print the numbers quoted in the README."""
    by_production, by_yield = rankings(df)

    print(f"rows            : {len(df):,}")
    print(f"crops           : {df['crop'].nunique():,}")
    print(f"states          : {df['state_name'].nunique():,}")
    print(f"years           : {int(df['crop_year'].min())}-{int(df['crop_year'].max())}")
    print()

    share = by_production.get(EXCLUDED_FROM_RANKING, 0) / df["production"].sum()
    print(
        f"{EXCLUDED_FROM_RANKING} alone accounts for {share:.1%} of summed production "
        "-> recorded in nuts, not tonnes, so it is excluded from the comparison"
    )
    print()

    comparable_prod = by_production.drop(EXCLUDED_FROM_RANKING)
    comparable_yield = by_yield.drop(EXCLUDED_FROM_RANKING)

    print(f"Top 10 by total production (excluding {EXCLUDED_FROM_RANKING}):")
    for name, value in comparable_prod.head(10).items():
        print(f"  {name:<28} {value:,.0f}")

    print()
    print(f"Top 10 by yield per hectare (excluding {EXCLUDED_FROM_RANKING}):")
    for name, value in comparable_yield.head(10).items():
        print(f"  {name:<28} {value:.1f}")

    print()
    top_prod = list(comparable_prod.head(10).index)
    top_yld = list(comparable_yield.head(10).index)
    shared = [c for c in top_prod if c in top_yld]
    print(f"shared between the two top-10 lists: {len(shared)} of 10 -> {shared}")

    rank_prod = {c: i + 1 for i, c in enumerate(comparable_prod.index)}
    rank_yld = {c: i + 1 for i, c in enumerate(comparable_yield.index)}
    swings = sorted(
        comparable_prod.head(20).index,
        key=lambda c: abs(rank_prod[c] - rank_yld[c]),
        reverse=True,
    )[:3]
    print()
    print("largest rank swings among the top 20 by production:")
    for c in swings:
        print(f"  {c:<28} production #{rank_prod[c]:<4} yield #{rank_yld[c]}")

    best_year = df.groupby("crop_year")["production"].sum().idxmax()
    print()
    print(f"highest total production year: {int(best_year)}")


def chart(df: pd.DataFrame, path: Path) -> None:
    """Save a two-panel comparison of the two rankings."""
    by_production, by_yield = rankings(df)
    prod = by_production.drop(EXCLUDED_FROM_RANKING).head(TOP_N)
    yld = by_yield.drop(EXCLUDED_FROM_RANKING).head(TOP_N)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), dpi=150)

    axes[0].barh(prod.index[::-1], prod.values[::-1] / 1e6, color="#2f6f4e")
    axes[0].set_title("Top crops by total production", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Production (million tonnes, summed 1997-2015)")

    axes[1].barh(yld.index[::-1], yld.values[::-1], color="#c2703d")
    axes[1].set_title("Top crops by yield per hectare", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Summed production / summed area")

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="x", alpha=0.25, linestyle=":")
        ax.tick_params(labelsize=9)

    fig.suptitle(
        "Same dataset, two metrics, four crops in common",
        fontsize=13, fontweight="bold", y=0.99,
    )
    fig.text(
        0.5, 0.005,
        "Coconut is excluded from both panels: the source records it in nuts, "
        "not tonnes, and it alone is 92% of summed production.",
        ha="center", fontsize=8, style="italic", color="#555555",
    )
    fig.tight_layout(rect=(0, 0.03, 1, 0.94))

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight")
    print(f"\nwrote {path}")


def main() -> None:
    df = load_clean()
    findings(df)
    chart(df, CHART_FILE)


if __name__ == "__main__":
    main()
