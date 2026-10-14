from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from ml.feature_engineering import make_tfidf


def train_engagement_model(data_path="data/processed/posts_processed.csv", artifact_path="ml/artifacts/engagement_model.joblib"):
    df = pd.read_csv(data_path)
    df = df.dropna(subset=["post_text", "engagement_rate"])
    df = df[(df["engagement_rate"] >= 0) & np.isfinite(df["engagement_rate"])]
    if len(df) < 30:
        raise ValueError("Not enough valid engagement records to train a regression model.")

    x_train, x_test, y_train, y_test = train_test_split(
        df["post_text"], df["engagement_rate"], test_size=0.25, random_state=42
    )
    model = Pipeline([("tfidf", make_tfidf()), ("reg", RandomForestRegressor(n_estimators=80, random_state=42))])
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    baseline = np.repeat(y_train.mean(), len(y_test))
    metrics = {
        "target": "engagement_rate",
        "features": ["post_text TF-IDF only; no reactions/comments/impressions leakage as inputs"],
        "mae": float(mean_absolute_error(y_test, predictions)),
        "rmse": float(root_mean_squared_error(y_test, predictions)),
        "r2": float(r2_score(y_test, predictions)),
        "baseline_mae": float(mean_absolute_error(y_test, baseline)),
        "limitation": "Small single-source dataset; exploratory model only.",
    }
    Path(artifact_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "metadata": metrics}, artifact_path)
    return metrics


if __name__ == "__main__":
    print(train_engagement_model())
