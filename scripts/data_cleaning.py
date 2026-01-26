import pandas as pd

# Load the raw dataset
df = pd.read_csv("D:\sustainable-farming-impact-dashboard/Crop Production data.csv")

# View first rows
print(df.head())

# Remove rows with missing Area or Production
df = df.dropna(subset=["Area", "Production"])

# Remove zero or negative values
df = df[(df["Area"] > 0) & (df["Production"] > 0)]

# Create Yield KPI
df["Yield_per_Hectare"] = df["Production"] / df["Area"]

# Save cleaned dataset
df.to_csv("D:\sustainable-farming-impact-dashboard/Crop Production data.csv", index=False)

print("STEP 2 COMPLETED: Clean data saved.")
