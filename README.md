# Sustainable Farming Impact Dashboard

Cleans and analyses crop production data to compare **yield efficiency** across crops — production per hectare rather than raw totals, which is what makes the comparison meaningful.

## Why yield per hectare

Production totals favour crops grown on more land. Dividing production by area gives a like-for-like comparison, so a small high-efficiency crop is not buried under a large low-efficiency one.

## Project structure

```
sustainable-farming-impact-dashboard/
├── scripts/
│   └── data_cleaning.py       # the cleaning pipeline
├── data/
│   ├── raw/                   # source dataset goes here (not committed)
│   └── processed/             # cleaned output (not committed)
├── requirements.txt
├── .gitignore
└── README.md
```

## How to run

1. Clone the repo and enter the folder:

   ```bash
   git clone https://github.com/sssfullstack007/sustainable-farming-impact-dashboard.git
   cd sustainable-farming-impact-dashboard
   ```

2. Install dependencies:

   ```bash
   py -m pip install -r requirements.txt
   ```

3. Put the source dataset in `data/raw/` under its original name,
   `Crop Production data.csv`. It is not committed to this repo because it is
   18 MB; download it from the source where you obtained it and place it there.

4. Run the pipeline:

   ```bash
   py scripts/data_cleaning.py
   ```

5. The cleaned file appears at `data/processed/crop_production_clean.csv`.

The script never modifies the raw file, so it can be re-run safely.

## What the script actually does

- Standardizes column names (lowercase, spaces to underscores)
- Validates that `area` and `production` exist, with a clear error if not
- Drops rows missing `area` or `production`
- Removes zero and negative area/production values
- Adds `yield_per_hectare = production / area`
- Writes to a separate processed file, creating folders as needed

Anything not implemented in code is not claimed here.

## Findings

Add three to five real observations from your own analysis here, for example:

> The top 10 crops by total production and by yield per hectare share only four crops,
> so a dashboard's ranking depends heavily on which metric is displayed.

## Notes

- The raw dataset is deliberately excluded from version control to keep the repo small.
- Earlier commits contain the raw CSV; repository history has not been rewritten.

## Skills demonstrated

Python, pandas, data cleaning, reproducible pipelines, Git.
