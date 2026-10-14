from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from ml.feature_engineering import make_tfidf

LABEL_KEYWORDS = {
    "technical education": ["tutorial", "learn", "build", "code", "framework", "pipeline", "database"],
    "project showcase": ["release", "project", "github", "docker", "app", "dataset"],
    "career advice": ["career", "tip", "journey", "advice", "interview"],
    "professional achievement": ["happy to share", "excited", "milestone", "stars"],
    "industry insight": ["year", "future", "trend", "industry", "ai"],
    "personal learning journey": ["i learned", "thinking", "experience"],
}


def weak_label(text):
    lowered = str(text).lower()
    scores = {
        label: sum(1 for keyword in keywords if keyword in lowered)
        for label, keywords in LABEL_KEYWORDS.items()
    }
    label, score = max(scores.items(), key=lambda item: item[1])
    return label if score else "technical education"


def train_classifier(data_path="data/processed/posts_processed.csv", artifact_path="ml/artifacts/post_classifier.joblib"):
    df = pd.read_csv(data_path)
    if "topic" not in df or df["topic"].isna().all():
        df["topic"] = df["post_text"].apply(weak_label)
    df = df.dropna(subset=["post_text", "topic"])
    if df["topic"].nunique() < 2 or len(df) < 10:
        raise ValueError("Not enough labeled data for a useful classifier.")

    min_class = df["topic"].value_counts().min()
    stratify = df["topic"] if min_class >= 2 else None
    x_train, x_test, y_train, y_test = train_test_split(
        df["post_text"], df["topic"], test_size=0.25, random_state=42, stratify=stratify
    )
    model = Pipeline([("tfidf", make_tfidf()), ("clf", LogisticRegression(max_iter=1000))])
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    metrics = {
        "classification_report": classification_report(y_test, predictions, zero_division=0, output_dict=True),
        "confusion_matrix": confusion_matrix(y_test, predictions).tolist(),
        "labels": sorted(df["topic"].unique().tolist()),
        "labeling_note": "Labels are weak heuristic labels for a reviewable baseline, not original dataset ground truth.",
    }
    Path(artifact_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "metadata": metrics}, artifact_path)
    return metrics


if __name__ == "__main__":
    print(train_classifier())
