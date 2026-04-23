import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ---------- load ----------
gen0 = pd.read_csv("gen0.csv")
gen1 = pd.read_csv("gen1.csv")

# ---------- clean ----------
# drop totally blank rows
gen0 = gen0.dropna(how="all").copy()
gen1 = gen1.dropna(how="all").copy()

# make sure score columns are numeric
gen0["complex_score"] = pd.to_numeric(gen0["complex_score"], errors="coerce")
gen1["complex_score"] = pd.to_numeric(gen1["complex_score"], errors="coerce")

# gen0 already has a proper category column
gen0["category_clean"] = gen0["category"].astype(str).str.strip()

# gen1 category is buried in enzyme_name like:
# "Alpha-glucosidase 2_alpha_glycans_"
def clean_cat_gen1(x):
    if pd.isna(x):
        return None
    x = str(x)

    for cat in ["alpha_glycans", "endoglucanases", "hemicelluloses", "polygalacturonases"]:
        if f"_{cat}_" in x or x.endswith(f"_{cat}") or cat in x:
            return cat
    return None

gen1["category_clean"] = gen1["enzyme_name"].apply(clean_cat_gen1)

# keep only usable rows
gen0 = gen0.dropna(subset=["category_clean", "complex_score"]).copy()
gen1 = gen1.dropna(subset=["category_clean", "complex_score"]).copy()

# label generations
gen0_plot = gen0[["category_clean", "complex_score"]].copy()
gen0_plot["generation"] = "gen0"

gen1_plot = gen1[["category_clean", "complex_score"]].copy()
gen1_plot["generation"] = "gen1"

df = pd.concat([gen0_plot, gen1_plot], ignore_index=True)

gen2 = pd.read_csv("gen2.csv")
gen2 = gen2.dropna(how="all").copy()

gen2["complex_score"] = pd.to_numeric(gen2["ranking_score"], errors="coerce")
gen2["category_clean"] = gen2["category"]

gen2_plot = gen2[["category_clean", "complex_score"]].copy()
gen2_plot["generation"] = "gen2"

df = pd.concat([df, gen2_plot], ignore_index=True)


# ---------- output folder ----------
outdir = Path("plots")
outdir.mkdir(exist_ok=True)

# ---------- 1) histograms by category ----------
for cat in sorted(df["category_clean"].unique()):
    subset = df[df["category_clean"] == cat]

    plt.figure(figsize=(8, 5))
    sns.histplot(
        data=subset,
        x="complex_score",
        hue="generation",
        bins=10,
        multiple="layer",
        alpha=0.5
    )
    plt.title(f"{cat}: score distribution by generation")
    plt.xlabel("complex_score")
    plt.ylabel("count")
    plt.tight_layout()
    plt.savefig(outdir / f"{cat}_hist.png", dpi=300)
    plt.close()

# ---------- 2) boxplot across categories ----------
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="category_clean", y="complex_score", hue="generation")
plt.xticks(rotation=20, ha="right")
plt.title("Score distributions by category and generation")
plt.xlabel("category")
plt.ylabel("complex_score")
plt.tight_layout()
plt.savefig(outdir / "all_categories_boxplot.png", dpi=300)
plt.close()

# ---------- 3) summary stats ----------
summary = (
    df.groupby(["category_clean", "generation"])["complex_score"]
    .agg(["count", "mean", "median", "std", "min", "max"])
    .round(3)
)

print(summary)
summary.to_csv(outdir / "summary_stats.csv")

print(f"\nSaved plots to: {outdir.resolve()}")
