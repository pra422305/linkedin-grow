HASHTAGS = {
    "technical education": ["#LearningInPublic", "#TechSkills", "#CareerGrowth"],
    "project showcase": ["#BuildInPublic", "#StudentDeveloper", "#Projects"],
    "career advice": ["#CareerAdvice", "#LinkedInForStudents", "#JobSearch"],
}


def generate_post(data):
    topic = data.get("topic", "a recent learning milestone").strip()
    audience = data.get("target_audience", "students and early-career professionals").strip()
    goal = data.get("career_goal", "grow professionally").strip()
    post_type = data.get("post_type", "Project showcase").strip()
    tone = data.get("tone", "Professional").strip()
    length = data.get("desired_length", "Medium").strip()
    experience = data.get("experience", "a hands-on project").strip()
    skills = data.get("skills", "problem solving, communication, and consistent learning").strip()

    hook = f"I used to think {topic} was just theory. Then I applied it in {experience}."
    body = [
        hook,
        "",
        f"Here is what I learned while working toward my goal to {goal}:",
        f"1. Start with a clear problem before choosing tools.",
        f"2. Use {skills} to turn vague ideas into visible progress.",
        "3. Document decisions, mistakes, and improvements so others can learn from the process.",
    ]
    if length.lower() != "short":
        body.extend(
            [
                "",
                f"For {audience}, the biggest takeaway is simple: small public proof of work compounds over time.",
                "A post does not need to be perfect. It should be honest, useful, and specific.",
            ]
        )
    body.extend(["", "What is one skill you are trying to show through your next project?"])

    tags = HASHTAGS.get(post_type.lower(), ["#LinkedInGrowth", "#ProfessionalDevelopment", "#Learning"])
    return {
        "draft": "\n".join(body + ["", " ".join(tags)]),
        "metadata": {"post_type": post_type, "tone": tone, "provider": "deterministic-template"},
    }
