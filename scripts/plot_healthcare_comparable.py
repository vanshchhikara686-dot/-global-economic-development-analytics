import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

file_path = (
    BASE_DIR / "outputs" /
    "healthcare_comparable_countries.csv"
)

df = pd.read_csv(file_path)

plt.figure(figsize=(12, 6))

plt.plot(
    df["Year"],
    df["Average_Expenditure"],
    marker="o",
    linewidth=2,
    label="Same 22 Countries"
)

plt.title(
    "Healthcare Expenditure Trend – "
    "Comparable Countries (2000–2024)",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Year")
plt.ylabel("Healthcare Expenditure (% of GDP)")

plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()

plt.tight_layout()

output_path = (
    BASE_DIR / "outputs" / "charts" /
    "healthcare_comparable_trend.png"
)

plt.savefig(output_path, dpi=300)
plt.show()

print("Comparable-country chart saved successfully!")