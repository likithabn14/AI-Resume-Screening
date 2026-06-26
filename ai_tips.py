def generate_ai_tips(matched_skills, missing_skills, ats_score):

    tips = []

    if matched_skills:
        tips.append(
            f"Your resume already matches {len(matched_skills)} important skill(s): "
            + ", ".join(matched_skills[:5]) + "."
        )

    if missing_skills:
        tips.append(
            "Consider adding these skills if they match your experience: "
            + ", ".join(missing_skills)
        )

    if ats_score < 60:
        tips.append(
            "Your ATS score is low. Improve your resume by adding projects, certifications, and relevant skills."
        )

    elif ats_score < 80:
        tips.append(
            "Your resume is good, but adding measurable achievements and missing skills can improve it further."
        )

    else:
        tips.append(
            "Excellent resume! Focus on tailoring it for each job description."
        )

    tips.append(
        "Include GitHub, LinkedIn, and a portfolio link."
    )

    tips.append(
        "Use action verbs like Developed, Built, Designed, Optimized, Implemented."
    )

    return tips