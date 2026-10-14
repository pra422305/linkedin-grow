from sklearn.feature_extraction.text import TfidfVectorizer


def make_tfidf(max_features=2000):
    return TfidfVectorizer(max_features=max_features, ngram_range=(1, 2), min_df=1, stop_words="english")
