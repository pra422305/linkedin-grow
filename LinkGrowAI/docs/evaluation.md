# Evaluation

Run evaluation after preparing the dataset:

```powershell
python -m ml.preprocess "https://huggingface.co/datasets/NeuML/neuml-linkedin-202501/resolve/main/posts.csv"
python -m ml.train_classifier
python -m ml.train_engagement_model
python -m ml.evaluate ml/artifacts/post_classifier.joblib
python -m ml.evaluate ml/artifacts/engagement_model.joblib
```

Interpret scores cautiously. The available dataset is small, single-source, and does not prove causal growth outcomes.

## Results From Local Run

Run date: 2026-10-14.

- Dataset preparation: processed 258 rows from the verified Hugging Face `posts.csv`.
- Classifier: accuracy `0.538`, macro F1 `0.410`. Labels were weak heuristic labels, not original dataset labels.
- Engagement regression: MAE `0.0148`, RMSE `0.0225`, R-squared `0.0855`, baseline MAE `0.0162`.

These results are suitable for a final-year exploratory prototype, not for production prediction claims.
