# Job Market Analyzer

A Python data analysis project that digs into a dataset of job postings to
find:

- **Top in-demand skills** — keyword search across job descriptions
  (Python, SQL, Excel, Tableau, etc.)
- **Salary trends** — average salary by state
- **Job locations** — where the postings are concentrated

## Dataset

Uses the [**Data Analyst Jobs**](https://www.kaggle.com/datasets/andrewmvd/data-analyst-jobs)
dataset on Kaggle — 2,253 data analyst job listings scraped from Glassdoor.
No live scraping needed; it's a static, ready-to-use CSV.

## Setup

1. Download `DataAnalyst.csv` from the Kaggle link above (free Kaggle
   account required)
2. Place it at `data/DataAnalyst.csv` in this project
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python analyze.py
```

This prints a summary to the console and saves results to `output/`:

| file | contents |
|---|---|
| `top_skills.csv` / `top_skills.png` | how often each skill is mentioned |
| `salary_by_state.csv` / `salary_by_state.png` | average salary ($K) per state |
| `jobs_by_state.csv` / `jobs_by_state.png` | number of postings per state |

## Notes

- The dataset uses `-1` as a placeholder for missing values; the script
  converts these to `NaN` automatically.
- To track a different skill set, edit the `SKILLS` list in `analyze.py`.
- To use a different (but similarly-shaped) dataset, update `DATA_FILE`
  and the column names referenced in `analyze.py`.
