from app.services.content_generator import generate_post
from app.services.networking_recommender import recommend_connections
from app.services.profile_analyzer import analyze_profile


def build_growth_plan(profile_data, feedback_count=0):
    analysis = analyze_profile(profile_data)
    topic = profile_data.get("target_role") or "career learning journey"
    draft = generate_post(
        {
            "topic": topic,
            "target_audience": "students and hiring managers",
            "career_goal": f"move toward {topic}",
            "post_type": "Project showcase",
            "tone": "Professional",
            "desired_length": "Medium",
            "experience": profile_data.get("projects") or "a recent project",
            "skills": profile_data.get("skills") or "Python, teamwork, communication",
        }
    )
    connections = recommend_connections(
        profile_data.get("skills", ""),
        profile_data.get("target_role", ""),
        profile_data.get("projects", ""),
    )
    tasks = [
        ("Monday", "Improve the headline and About section using the profile suggestions."),
        ("Tuesday", f"Publish or refine one post about {topic}."),
        ("Wednesday", "Comment thoughtfully on three posts in your target domain."),
        ("Thursday", "Send two personalized connection requests from the recommendation list."),
        ("Friday", "Add metrics or screenshots to one project description."),
        ("Saturday", "Enter this week's post metrics into analytics."),
        ("Sunday", "Review feedback and choose next week's topic."),
    ]
    return {
        "profile_analysis": analysis,
        "recommended_topic": topic,
        "post_draft": draft["draft"],
        "connections": connections,
        "tasks": tasks,
        "reason": "The plan prioritizes missing profile sections, visible proof of work, and measured networking actions.",
        "feedback_note": f"Future recommendations can use {feedback_count} saved feedback records, but no automatic retraining is claimed.",
    }
