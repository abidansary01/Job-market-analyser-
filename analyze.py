"""
analyze.py

Analyzes a job postings dataset to surface:
  - Top in-demand skills (keyword search across job descriptions)
  - Average salary by state
  - Job posting counts by state

Dataset used: "Data Analyst Jobs" by andrewmvd on Kaggle
https://www.kaggle.com/datasets/andrewmvd/data-analyst-jobs
(2,253 data analyst job listings scraped from Glassdoor)

Setup:
    1. Download DataAnalyst.csv from the Kaggle link above
    2. Place it at: data/DataAnalyst.csv
    3. Run: python analyze.py
"""

import os
import re

import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = "data/DataAnalyst.csv"
OUTPUT_DIR = "output"

# Skills to search for in job descriptions. Add/remove as you like.
SKILLS = [
    "Python", "SQL", "Excel", "Tableau", "R", "SAS", "Power BI",
    "AWS", "Spark", "Java", "Hadoop", "Machine Learning", "SPSS",
]


def load_data(path=DATA_FILE):
    df = pd.read_csv(path)
    # This dataset uses -1 as a placeholder for missing values
    df = df.replace(-1, pd.NA).replace("-1", pd.NA)
    return df


def clean_salary(df):
    """Parse 'Salary Estimate' (e.g. '$37K-$66K (Glassdoor est.)') into numeric $K columns."""
    def parse(value):
        if pd.isna(value):
            return pd.Series([None, None, None])
        nums = re.findall(r"(\d+)K", str(value))
        if len(nums) == 2:
            lo, hi = int(nums[0]), int(nums[1])
            return pd.Series([lo, hi, (lo + hi) / 2])
        return pd.Series([None, None, None])

    df[["salary_min_k", "salary_max_k", "salary_avg_k"]] = df["Salary Estimate"].apply(parse)
    return df


def clean_location(df):
    """Split 'City, ST' into separate city/state columns."""
    split = df["Location"].str.split(",", n=1, expand=True)
    df["city"] = split[0].str.strip()
    df["state"] = split[1].str.strip() if split.shape[1] > 1 else None
    return df


def extract_skills(df):
    """Count how many job postings mention each skill in the description."""
    counts = {}
    descriptions = df["Job Description"].fillna("")
    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        counts[skill] = descriptions.str.contains(pattern, case=False, regex=True).sum()
    return pd.Series(counts).sort_values(ascending=False)


def salary_by_state(df):
    return (
        df.dropna(subset=["salary_avg_k", "state"])
        .groupby("state")["salary_avg_k"]
        .mean()
        .sort_values(ascending=False)
    )


def jobs_by_state(df):
    return df["state"].value_counts()


def save_bar_chart(series, title, ylabel, filename, top_n=10):
    plt.figure(figsize=(10, 6))
    series.head(top_n).plot(kind="bar")
    plt.title(title)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename))
    plt.close()


def run():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = load_data()
    df = clean_salary(df)
    df = clean_location(df)

    print(f"Loaded {len(df)} job listings\n")

    skills = extract_skills(df)
    print("Top skills mentioned in job descriptions:")
    print(skills, "\n")
    skills.to_csv(os.path.join(OUTPUT_DIR, "top_skills.csv"), header=["mentions"])
    save_bar_chart(skills, "Most In-Demand Skills", "Number of job postings", "top_skills.png")

    state_salary = salary_by_state(df)
    print("Average salary by state (top 10):")
    print(state_salary.head(10), "\n")
    state_salary.to_csv(os.path.join(OUTPUT_DIR, "salary_by_state.csv"), header=["avg_salary_k"])
    save_bar_chart(state_salary, "Average Salary by State ($K)", "Average salary ($K)", "salary_by_state.png")

    state_counts = jobs_by_state(df)
    print("Job postings by state (top 10):")
    print(state_counts.head(10), "\n")
    state_counts.to_csv(os.path.join(OUTPUT_DIR, "jobs_by_state.csv"), header=["job_count"])
    save_bar_chart(state_counts, "Job Postings by State", "Number of postings", "jobs_by_state.png")

    print(f"Charts and CSV summaries saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    run()
