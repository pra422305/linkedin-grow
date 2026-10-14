SECTION_WEIGHTS = {
    "linkedin_profile_url": 5,
    "headline": 15,
    "about": 20,
    "skills": 15,
    "education": 10,
    "projects": 15,
    "experience": 15,
    "target_role": 5,
}


def _present(value):
    return bool(value and str(value).strip())


def analyze_profile(profile_data):
    score = 0
    missing = []
    for field, weight in SECTION_WEIGHTS.items():
        if _present(profile_data.get(field)):
            score += weight
        else:
            missing.append(field.replace("_", " ").title())

    headline = profile_data.get("headline", "").strip()
    target_role = profile_data.get("target_role", "").strip() or "your target role"
    skills = [s.strip() for s in profile_data.get("skills", "").replace("\n", ",").split(",") if s.strip()]
    top_skills = ", ".join(skills[:3]) if skills else "your strongest skills"

    suggestions = [
        f"Rewrite the headline around {target_role} and show 2-3 proof points.",
        "Add measurable outcomes to projects, for example tools used, users served, or accuracy achieved.",
        "Use the About section to connect your background, strengths, and current goal.",
        "Use the LinkedIn profile URL as the profile identity for saved recommendations and manual analytics imports.",
    ]
    if not _present(profile_data.get("linkedin_profile_url")):
        suggestions.append("Add your LinkedIn profile URL so drafts and plans can refer to the correct profile.")
    if headline and target_role.lower() not in headline.lower():
        suggestions.append(f"Include the target role phrase '{target_role}' in the headline.")

    improved_about = (
        f"I am building toward {target_role}, with hands-on experience in {top_skills}. "
        "I enjoy turning academic projects into practical, user-focused solutions and documenting what I learn. "
        "My current focus is improving my portfolio, sharing useful work publicly, and connecting with professionals "
        "who care about applied technology."
    )

    return {
        "score": min(score, 100),
        "missing": missing,
        "headline_suggestions": [
            f"{target_role} | {top_skills} | Project-driven learner",
            f"Aspiring {target_role} focused on {top_skills}",
        ],
        "improved_about": improved_about,
        "recommendations": suggestions,
        "disclaimer": (
            "This is a transparent LinkGrow AI score, not an official LinkedIn score. "
            "A profile URL alone cannot provide private profile-view analytics; use manual entry or authorized exports."
        ),
    }
