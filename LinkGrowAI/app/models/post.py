from app import db


class SavedPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    topic = db.Column(db.String(180), nullable=False)
    post_type = db.Column(db.String(80), default="Educational")
    tone = db.Column(db.String(80), default="Professional")
    draft_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", backref=db.backref("saved_posts", cascade="all, delete-orphan"))
