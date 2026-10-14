from flask import Blueprint, flash, render_template, request
from flask_login import current_user, login_required

from app import db
from app.models.user import UserProfile
from app.services.profile_analyzer import analyze_profile

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.route("/", methods=["GET", "POST"])
@login_required
def profile():
    profile = current_user.profile or UserProfile(user_id=current_user.id)
    analysis = None
    if request.method == "POST":
        fields = [
            "headline",
            "about",
            "skills",
            "education",
            "projects",
            "experience",
            "target_role",
            "linkedin_profile_url",
        ]
        for field in fields:
            setattr(profile, field, request.form.get(field, "").strip())
        if profile.linkedin_profile_url and "linkedin.com/in/" not in profile.linkedin_profile_url.lower():
            flash("Enter a valid LinkedIn profile URL, for example https://www.linkedin.com/in/your-name.", "danger")
            return render_template("profile.html", profile=profile, analysis=None)
        analysis = analyze_profile({field: getattr(profile, field) for field in fields})
        profile.profile_score = analysis["score"]
        db.session.add(profile)
        db.session.commit()
        flash("Profile analyzed and saved.", "success")
    elif current_user.profile:
        fields = [
            "headline",
            "about",
            "skills",
            "education",
            "projects",
            "experience",
            "target_role",
            "linkedin_profile_url",
        ]
        analysis = analyze_profile({field: getattr(profile, field) for field in fields})
    return render_template("profile.html", profile=profile, analysis=analysis)
