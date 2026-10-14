from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.models.analytics import AnalyticsRecord
from app.models.post import SavedPost
from app.services.engagement_analyzer import summarize_records

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("dashboard.html", summary=_summary())
    return render_template("index.html")


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", summary=_summary())


def _summary():
    profile_score = current_user.profile.profile_score if current_user.profile else 0
    records = AnalyticsRecord.query.filter_by(user_id=current_user.id).all()
    total_likes = sum((record.reactions or 0) for record in records)
    total_impressions = sum((record.impressions or 0) for record in records)
    total_reposts = sum((record.reposts or 0) for record in records)
    new_connections = sum((record.new_connections or 0) for record in records)
    top_posts = sorted(
        records,
        key=lambda record: (record.reactions or 0) + (record.comments or 0) + (record.reposts or 0),
        reverse=True,
    )[:5]
    return {
        "profile_score": profile_score,
        "saved_posts": SavedPost.query.filter_by(user_id=current_user.id).count(),
        "analytics": summarize_records(records),
        "linkedin_profile_url": current_user.profile.linkedin_profile_url if current_user.profile else "",
        "total_likes": total_likes,
        "total_impressions": total_impressions,
        "total_reposts": total_reposts,
        "new_connections": new_connections,
        "top_posts": top_posts,
        "chart_data": [
            {
                "date": record.post_date.isoformat(),
                "topic": record.topic,
                "impressions": record.impressions or 0,
                "reactions": record.reactions or 0,
                "comments": record.comments or 0,
                "reposts": record.reposts or 0,
            }
            for record in sorted(records, key=lambda item: item.post_date)
        ],
    }
