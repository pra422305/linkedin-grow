from tests.conftest import register_and_login


def test_index_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"LinkGrow AI" in response.data


def test_auth_and_profile_flow(client):
    register_and_login(client)
    response = client.post(
        "/profile/",
        data={
            "headline": "Aspiring ML Engineer",
            "about": "I build projects.",
            "skills": "Python, Flask, ML",
            "education": "Computer Engineering",
            "projects": "LinkGrow AI",
            "experience": "Internship",
            "target_role": "ML Engineer",
            "linkedin_profile_url": "https://www.linkedin.com/in/test-user",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Profile analyzed" in response.data


def test_content_and_analytics_routes(client):
    register_and_login(client)
    response = client.post(
        "/content/",
        data={"topic": "Flask project", "skills": "Python", "action": "generate"},
        follow_redirects=True,
    )
    assert b"Editable Draft" in response.data
    response = client.post(
        "/analytics/",
        data={
            "post_date": "2026-01-01",
            "topic": "Project",
            "post_format": "Text",
            "impressions": "100",
            "reactions": "5",
            "comments": "2",
            "reposts": "1",
        },
        follow_redirects=True,
    )
    assert b"Analytics record saved" in response.data
