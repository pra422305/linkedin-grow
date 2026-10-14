def calculate_engagement_rate(impressions, reactions, comments, reposts):
    total = (reactions or 0) + (comments or 0) + (reposts or 0)
    if impressions is None or impressions <= 0:
        return None
    return round(total / impressions, 4)


def summarize_records(records):
    if not records:
        return {"count": 0, "avg_engagement_rate": None, "total_interactions": 0}
    rates = [r.engagement_rate for r in records if r.engagement_rate is not None]
    interactions = sum((r.reactions or 0) + (r.comments or 0) + (r.reposts or 0) for r in records)
    return {
        "count": len(records),
        "avg_engagement_rate": round(sum(rates) / len(rates), 4) if rates else None,
        "total_interactions": interactions,
    }
