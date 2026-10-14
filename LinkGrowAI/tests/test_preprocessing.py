import pandas as pd

from ml.preprocess import clean_text, standardize_dataframe


def test_clean_text_normalizes_whitespace():
    assert clean_text("  Hello\n\nLinkedIn   ") == "Hello LinkedIn"


def test_standardize_dataframe_handles_missing_and_duplicates():
    df = pd.DataFrame(
        {
            "Post title": [" First post ", " First post ", ""],
            "Post link": ["a", "a", "b"],
            "Impressions": ["1,000", "-5", "10"],
            "Likes": [10, 10, 1],
            "Comments": [2, 2, 0],
            "Reposts": [1, 1, 0],
            "Engagement rate": [0.013, 0.013, 0.1],
        }
    )
    processed, report = standardize_dataframe(df)
    assert len(processed) == 1
    assert processed.iloc[0]["post_text"] == "First post"
    assert report["removed_empty_text"] == 1
    assert report["removed_duplicates"] == 1
