import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'instance' / 'linkgrow_dev.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "")
    LLM_API_KEY = os.getenv("LLM_API_KEY", "")
    LLM_MODEL = os.getenv("LLM_MODEL", "")
    DATASET_URL = os.getenv(
        "LINKGROW_DATASET_URL",
        "https://huggingface.co/datasets/NeuML/neuml-linkedin-202501/resolve/main/posts.csv",
    )
    RANDOM_SEED = int(os.getenv("RANDOM_SEED", "42"))


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
