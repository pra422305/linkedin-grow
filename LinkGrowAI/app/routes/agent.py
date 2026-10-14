from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models.recommendation import Feedback, GrowthTask, Recommendation
from app.services.growth_agent import build_growth_plan

agent_bp = Blueprint("agent", __name__, url_prefix="/agent")


@agent_bp.route("/", methods=["GET", "POST"])
@login_required
def growth_plan():
    profile = current_user.profile
    profile_data = {
        "headline": profile.headline if profile else "",
        "about": profile.about if profile else "",
        "skills": profile.skills if profile else "",
        "education": profile.education if profile else "",
        "projects": profile.projects if profile else "",
        "experience": profile.experience if profile else "",
        "target_role": profile.target_role if profile else request.form.get("career_goal", ""),
        "linkedin_profile_url": profile.linkedin_profile_url if profile else "",
    }
    feedback_count = Feedback.query.filter_by(user_id=current_user.id).count()
    plan = build_growth_plan(profile_data, feedback_count)
    if request.method == "POST":
        Recommendation.query.filter_by(user_id=current_user.id, category="growth_plan").delete()
        GrowthTask.query.filter_by(user_id=current_user.id).delete()
        db.session.add(Recommendation(user_id=current_user.id, category="growth_plan", text=plan["recommended_topic"], reason=plan["reason"]))
        for day, task in plan["tasks"]:
            db.session.add(GrowthTask(user_id=current_user.id, day=day, task=task))
        db.session.commit()
        flash("Weekly growth plan saved.", "success")
    tasks = GrowthTask.query.filter_by(user_id=current_user.id).all()
    return render_template("growth_plan.html", plan=plan, tasks=tasks)


@agent_bp.route("/task/<int:task_id>/toggle", methods=["POST"])
@login_required
def toggle_task(task_id):
    task = GrowthTask.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for("agent.growth_plan"))


@agent_bp.route("/feedback", methods=["POST"])
@login_required
def feedback():
    rating = int(request.form.get("rating", "3"))
    db.session.add(Feedback(user_id=current_user.id, rating=max(1, min(5, rating)), comment=request.form.get("comment", "")))
    db.session.commit()
    flash("Feedback saved for future recommendation tuning.", "success")
    return redirect(url_for("agent.growth_plan"))
