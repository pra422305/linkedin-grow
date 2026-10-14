from pathlib import Path

import pandas as pd

VERIFIED_DATASET = {
    "name": "NeuML neuml-linkedin-202501",
    "source": "https://huggingface.co/datasets/NeuML/neuml-linkedin-202501",
    "file": "posts.csv",
    "license": "apache-2.0",
    "verified_on": "2026-10-14",
}


def load_dataset(path_or_url):
    if not path_or_url:
        raise ValueError("Provide a local CSV path or dataset URL.")
    return pd.read_csv(path_or_url)


def inspect_dataset(df):
    return {
        "records": int(len(df)),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing": {col: int(df[col].isna().sum()) for col in df.columns},
        "duplicates": int(df.duplicated().sum()),
    }


def save_report(report, output_path):
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Dataset Report", ""]
    for key, value in report.items():
        lines.append(f"## {key}")
        lines.append(str(value))
        lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")
