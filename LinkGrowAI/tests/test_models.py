import pandas as pd

from app import db
from app.models.analytics import AnalyticsRecord
from app.models.user import User


def test_user_password_hashing(app):
    with app.app_context():
        user = User(name="A", email="a@example.com")
        user.set_password("secret123")
        assert user.password_hash != "secret123"
        assert user.check_password("secret123")


def test_analytics_model_persists(app):
    with app.app_context():
        user = User(name="A", email="a@example.com")
        user.set_password("secret123")
        db.session.add(user)
        db.session.commit()
        record = AnalyticsRecord(
            user_id=user.id,
            post_date=pd.Timestamp("2026-01-01").date(),
            topic="ML",
            impressions=100,
            reactions=5,
            comments=1,
            reposts=1,
            engagement_rate=0.07,
        )
        db.session.add(record)
        db.session.commit()
        assert AnalyticsRecord.query.count() == 1
