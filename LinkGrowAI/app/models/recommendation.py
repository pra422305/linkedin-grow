from app import db


class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    category = db.Column(db.String(80), nullable=False)
    text = db.Column(db.Text, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default="suggested")
    created_at = db.Column(db.DateTime, server_default=db.func.now())


class GrowthTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    day = db.Column(db.String(20), nullable=False)
    task = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    recommendation_id = db.Column(db.Integer, db.ForeignKey("recommendation.id"), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
