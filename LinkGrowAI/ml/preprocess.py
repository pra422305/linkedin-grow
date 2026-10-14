import re
from pathlib import Path

import pandas as pd

from ml.data_loader import VERIFIED_DATASET, inspect_dataset, load_dataset, save_report

COLUMN_MAP = {
    "Post title": "post_text",
    "Post link": "post_id",
    "Post type": "post_format",
    "Posted by": "creator_or_page_id",
    "Created date": "publication_date",
    "Impressions": "impressions",
    "Likes": "reactions",
    "Comments": "comments",
    "Reposts": "reposts",
    "Engagement rate": "engagement_rate",
    "Clicks": "clicks",
    "Click through rate (CTR)": "click_through_rate",
}

STANDARD_COLUMNS = [
    "post_id",
    "post_text",
    "creator_or_page_id",
    "topic",
    "hook_type",
    "post_format",
    "publication_date",
    "impressions",
    "reactions",
    "comments",
    "reposts",
    "engagement_rate",
    "source",
    "license_or_permission_reference",
]


def clean_text(value):
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def parse_numeric(series):
    return pd.to_numeric(series.astype(str).str.replace(",", "", regex=False), errors="coerce")


def standardize_dataframe(df):
    report = {"initial": inspect_dataset(df)}
    work = df.rename(columns={col: COLUMN_MAP[col] for col in df.columns if col in COLUMN_MAP}).copy()
    for col in STANDARD_COLUMNS:
        if col not in work.columns:
            work[col] = pd.NA

    work["post_text"] = work["post_text"].apply(clean_text)
    before_empty = len(work)
    work = work[work["post_text"].str.len() > 0].copy()
    report["removed_empty_text"] = before_empty - len(work)

    before_dupes = len(work)
    work = work.drop_duplicates(subset=["post_id", "post_text"], keep="first")
    report["removed_duplicates"] = before_dupes - len(work)

    for col in ["impressions", "reactions", "comments", "reposts", "engagement_rate"]:
        work[col] = parse_numeric(work[col])
        work.loc[work[col] < 0, col] = pd.NA

    work["publication_date"] = pd.to_datetime(work["publication_date"], errors="coerce")
    work["source"] = VERIFIED_DATASET["source"]
    work["license_or_permission_reference"] = VERIFIED_DATASET["license"]
    report["final"] = inspect_dataset(work[STANDARD_COLUMNS])
    report["numeric_summary"] = work[["impressions", "reactions", "comments", "reposts", "engagement_rate"]].describe().to_dict()
    report["limitations"] = (
        "This dataset is small and appears to represent posts from one creator/page. "
        "Use results as exploratory patterns, not proof of causal LinkedIn growth."
    )
    return work[STANDARD_COLUMNS], report


def prepare_dataset(input_path, output_path="data/processed/posts_processed.csv", report_path="docs/dataset_report.md"):
    df = load_dataset(input_path)
    processed, report = standardize_dataframe(df)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    processed.to_csv(output_path, index=False)
    save_report(report, report_path)
    return processed, report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Local CSV path or URL")
    parser.add_argument("--output", default="data/processed/posts_processed.csv")
    parser.add_argument("--report", default="docs/dataset_report.md")
    args = parser.parse_args()
    processed_df, prep_report = prepare_dataset(args.input, args.output, args.report)
    print(f"Prepared {len(processed_df)} rows -> {args.output}")
