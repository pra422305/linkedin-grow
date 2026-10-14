from app.services.engagement_analyzer import calculate_engagement_rate
from app.services.networking_recommender import recommend_connections
from app.services.profile_analyzer import analyze_profile


def test_profile_score_and_missing_sections():
    result = analyze_profile({"headline": "AI Student", "skills": "Python", "target_role": "ML Engineer"})
    assert result["score"] > 0
    assert "About" in result["missing"]


def test_networking_returns_ranked_sample_profiles():
    results = recommend_connections("Python Flask ML", "ML Engineer")
    assert len(results) == 3
    assert results[0]["score"] >= results[-1]["score"]
    assert "message" in results[0]


def test_engagement_rate_handles_zero_impressions():
    assert calculate_engagement_rate(0, 1, 1, 1) is None
    assert calculate_engagement_rate(100, 5, 3, 2) == 0.1
