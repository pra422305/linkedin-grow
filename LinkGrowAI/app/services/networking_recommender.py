from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SAMPLE_PROFILES = [
    {
        "name": "Sample Mentor A",
        "industry": "AI/ML",
        "skills": "Python machine learning scikit-learn NLP Flask",
        "interests": "student projects model evaluation responsible AI",
    },
    {
        "name": "Sample Peer B",
        "industry": "Full Stack",
        "skills": "JavaScript Bootstrap Flask SQL dashboards",
        "interests": "portfolio projects internships web apps",
    },
    {
        "name": "Sample Recruiter C",
        "industry": "Technology Hiring",
        "skills": "entry level hiring resumes career advice communication",
        "interests": "freshers internships interview preparation",
    },
    {
        "name": "Sample Data Analyst D",
        "industry": "Analytics",
        "skills": "SQL pandas visualization Chart.js metrics",
        "interests": "business dashboards engagement analysis",
    },
]


def recommend_connections(skills, target_role, interests="", limit=3):
    query = f"{skills} {target_role} {interests}".strip() or "student software projects"
    documents = [query] + [f"{p['industry']} {p['skills']} {p['interests']}" for p in SAMPLE_PROFILES]
    matrix = TfidfVectorizer(stop_words="english").fit_transform(documents)
    scores = cosine_similarity(matrix[0], matrix[1:]).flatten()
    ranked = sorted(zip(SAMPLE_PROFILES, scores), key=lambda item: item[1], reverse=True)[:limit]

    results = []
    for profile, score in ranked:
        message = (
            f"Hi, I noticed your work around {profile['industry']}. "
            f"I am building toward {target_role or 'a technology role'} and learning through projects. "
            "I would value connecting and following your insights."
        )
        results.append(
            {
                **profile,
                "score": round(float(score), 3),
                "explanation": f"Matched on skills/interests related to {profile['industry']}.",
                "message": message,
            }
        )
    return results
