from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models.analytics import AnalyticsRecord
from app.services.engagement_analyzer import calculate_engagement_rate, summarize_records
from app.services.linkedin_connector import LinkedInConnectorError, connection_status, fetch_authorized_metrics

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")


@analytics_bp.route("/", methods=["GET", "POST"])
@login_required
def analytics():
    if request.method == "POST":
        try:
            impressions = _int_or_none(request.form.get("impressions"))
            record = AnalyticsRecord(
                user_id=current_user.id,
                post_date=datetime.strptime(request.form.get("post_date"), "%Y-%m-%d").date(),
                topic=request.form.get("topic", "").strip() or "Untitled",
                post_format=request.form.get("post_format", "Text"),
                impressions=impressions,
                reactions=_int_or_zero(request.form.get("reactions")),
                comments=_int_or_zero(request.form.get("comments")),
                reposts=_int_or_zero(request.form.get("reposts")),
                profile_views=_int_or_none(request.form.get("profile_views")),
                new_connections=_int_or_none(request.form.get("new_connections")),
                linkedin_post_url=request.form.get("linkedin_post_url", "").strip(),
                source="manual",
            )
            record.engagement_rate = calculate_engagement_rate(
                record.impressions, record.reactions, record.comments, record.reposts
            )
            db.session.add(record)
            db.session.commit()
            flash("Analytics record saved.", "success")
        except ValueError:
            flash("Check the date and numeric metric fields.", "danger")
    records = AnalyticsRecord.query.filter_by(user_id=current_user.id).order_by(AnalyticsRecord.post_date).all()
    chart_data = _build_chart_data(records)
    return render_template(
        "analytics.html",
        records=records,
        summary=summarize_records(records),
        chart_data=chart_data,
        linkedin_status=connection_status(current_user.profile.linkedin_profile_url if current_user.profile else ""),
    )


@analytics_bp.route("/sync-linkedin", methods=["POST"])
@login_required
def sync_linkedin():
    profile_url = current_user.profile.linkedin_profile_url if current_user.profile else ""
    try:
        result = fetch_authorized_metrics(profile_url)
        imported = 0
        for row in result["records"]:
            record = AnalyticsRecord(
                user_id=current_user.id,
                post_date=row["post_date"],
                topic=row.get("topic", "LinkedIn post"),
                post_format=row.get("post_format", "LinkedIn"),
                impressions=row.get("impressions"),
                reactions=row.get("reactions", 0),
                comments=row.get("comments", 0),
                reposts=row.get("reposts", 0),
                profile_views=row.get("profile_views"),
                new_connections=row.get("new_connections"),
                linkedin_post_url=row.get("linkedin_post_url", ""),
                source="linkedin_api",
            )
            record.engagement_rate = calculate_engagement_rate(
                record.impressions, record.reactions, record.comments, record.reposts
            )
            db.session.add(record)
            imported += 1
        db.session.commit()
        flash(f"LinkedIn sync completed. Imported {imported} genuine metric records.", "success")
    except LinkedInConnectorError as exc:
        flash(str(exc), "warning")
    return redirect(url_for("analytics.analytics"))


def _build_chart_data(records):
    points = [
        {
            "date": r.post_date.isoformat(),
            "topic": r.topic,
            "format": r.post_format,
            "rate": r.engagement_rate,
            "impressions": r.impressions or 0,
            "reactions": r.reactions or 0,
            "comments": r.comments or 0,
            "reposts": r.reposts or 0,
            "profile_views": r.profile_views or 0,
            "new_connections": r.new_connections or 0,
            "interactions": (r.reactions or 0) + (r.comments or 0) + (r.reposts or 0),
        }
        for r in records
    ]
    totals = {
        "impressions": sum(row["impressions"] for row in points),
        "reactions": sum(row["reactions"] for row in points),
        "comments": sum(row["comments"] for row in points),
        "reposts": sum(row["reposts"] for row in points),
        "profile_views": sum(row["profile_views"] for row in points),
        "new_connections": sum(row["new_connections"] for row in points),
    }
    return {"points": points, "totals": totals}


def _int_or_zero(value):
    return int(value or 0)


def _int_or_none(value):
    return None if value in (None, "") else int(value)
