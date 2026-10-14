import joblib


def predict_topic(text, artifact_path="ml/artifacts/post_classifier.joblib"):
    artifact = joblib.load(artifact_path)
    return artifact["model"].predict([text])[0]


def predict_engagement(text, artifact_path="ml/artifacts/engagement_model.joblib"):
    artifact = joblib.load(artifact_path)
    return float(artifact["model"].predict([text])[0])
