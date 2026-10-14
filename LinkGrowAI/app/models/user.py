from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    profile = db.relationship("UserProfile", backref="user", uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    headline = db.Column(db.String(220), default="")
    about = db.Column(db.Text, default="")
    skills = db.Column(db.Text, default="")
    education = db.Column(db.Text, default="")
    projects = db.Column(db.Text, default="")
    experience = db.Column(db.Text, default="")
    target_role = db.Column(db.String(160), default="")
    linkedin_profile_url = db.Column(db.String(500), default="")
    profile_score = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
