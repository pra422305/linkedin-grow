from flask import Blueprint, flash, render_template, request
from flask_login import current_user, login_required

from app import db
from app.models.post import SavedPost
from app.services.content_generator import generate_post

content_bp = Blueprint("content", __name__, url_prefix="/content")


@content_bp.route("/", methods=["GET", "POST"])
@login_required
def content_generator():
    draft = None
    if request.method == "POST":
        action = request.form.get("action")
        data = request.form.to_dict()
        draft_text = request.form.get("draft_text", "").strip()
        if action == "save" and draft_text:
            post = SavedPost(
                user_id=current_user.id,
                topic=data.get("topic", "Untitled"),
                post_type=data.get("post_type", "Educational"),
                tone=data.get("tone", "Professional"),
                draft_text=draft_text,
            )
            db.session.add(post)
            db.session.commit()
            flash("Draft saved.", "success")
            draft = {"draft": draft_text}
        else:
            draft = generate_post(data)
    saved = SavedPost.query.filter_by(user_id=current_user.id).order_by(SavedPost.created_at.desc()).all()
    return render_template("content_generator.html", draft=draft, saved=saved)
