from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from app.services.networking_recommender import recommend_connections

networking_bp = Blueprint("networking", __name__, url_prefix="/networking")


@networking_bp.route("/", methods=["GET", "POST"])
@login_required
def networking():
    profile = current_user.profile
    skills = request.form.get("skills") or (profile.skills if profile else "")
    target_role = request.form.get("target_role") or (profile.target_role if profile else "")
    interests = request.form.get("interests", "")
    recommendations = recommend_connections(skills, target_role, interests) if request.method == "POST" or profile else []
    return render_template(
        "networking.html",
        recommendations=recommendations,
        skills=skills,
        target_role=target_role,
        interests=interests,
    )
