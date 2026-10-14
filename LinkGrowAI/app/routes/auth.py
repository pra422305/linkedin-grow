from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app import db
from app.models.user import User
from app.models.user import UserProfile

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").lower().strip()
        password = request.form.get("password", "")
        linkedin_profile_url = request.form.get("linkedin_profile_url", "").strip()
        if not name or "@" not in email or len(password) < 8:
            flash("Enter a name, valid email, and password of at least 8 characters.", "danger")
        elif linkedin_profile_url and "linkedin.com/in/" not in linkedin_profile_url.lower():
            flash("Enter a valid LinkedIn profile URL, for example https://www.linkedin.com/in/your-name.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "danger")
        else:
            user = User(name=name, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            db.session.add(UserProfile(user_id=user.id, linkedin_profile_url=linkedin_profile_url))
            db.session.commit()
            login_user(user)
            return redirect(url_for("dashboard.dashboard"))
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").lower().strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("dashboard.dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return redirect(url_for("dashboard.index"))
