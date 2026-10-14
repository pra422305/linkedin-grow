from app import db


class AnalyticsRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    post_date = db.Column(db.Date, nullable=False)
    topic = db.Column(db.String(180), nullable=False)
    post_format = db.Column(db.String(80), default="Text")
    impressions = db.Column(db.Integer, nullable=True)
    reactions = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    reposts = db.Column(db.Integer, default=0)
    engagement_rate = db.Column(db.Float, nullable=True)
    profile_views = db.Column(db.Integer, nullable=True)
    new_connections = db.Column(db.Integer, nullable=True)
    linkedin_post_url = db.Column(db.String(500), default="")
    source = db.Column(db.String(40), default="manual")
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", backref=db.backref("analytics_records", cascade="all, delete-orphan"))
