# Model Card

## Post Pattern Classifier

The baseline classifier uses TF-IDF features and logistic regression. If human labels are unavailable, the script creates weak heuristic labels and records that limitation in metadata. These labels are intended for a reviewable classroom baseline, not as ground truth.

## Engagement Model

The engagement model uses TF-IDF text features and a random forest regressor to predict the verified `engagement_rate` column only when enough valid rows exist. It avoids using impressions, reactions, comments, or reposts as inputs because those values would leak the target.

Both scripts save artifacts with evaluation metadata under `ml/artifacts/`.
