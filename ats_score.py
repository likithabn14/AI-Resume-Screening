import re

def calculate_ats_score(resume_text, matched_skills, missing_skills):

    score = 0
    suggestions = []
    checks = {}

    text = resume_text.lower()

    # ======================================
    # Skill Match (40 Marks)
    # ======================================

    total_skills = len(matched_skills) + len(missing_skills)

    if total_skills > 0:
        skill_score = round(
            (len(matched_skills) / total_skills) * 40
        )
    else:
        skill_score = 20

    score += skill_score

    # ======================================
    # Contact Information (10)
    # ======================================

    email = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        resume_text
    )

    phone = re.search(r"\d{10}", resume_text)

    checks["Contact Information"] = bool(email and phone)

    if checks["Contact Information"]:
        score += 10
    else:
        suggestions.append(
            "Add your email address and phone number."
        )

    # ======================================
    # Education (10)
    # ======================================

    checks["Education"] = "education" in text

    if checks["Education"]:
        score += 10
    else:
        suggestions.append(
            "Add an Education section."
        )

    # ======================================
    # Experience (10)
    # ======================================

    checks["Experience"] = "experience" in text

    if checks["Experience"]:
        score += 10
    else:
        suggestions.append(
            "Add an Experience section."
        )

    # ======================================
    # Projects (10)
    # ======================================

    checks["Projects"] = "project" in text

    if checks["Projects"]:
        score += 10
    else:
        suggestions.append(
            "Add a Projects section."
        )

    # ======================================
    # Certifications (10)
    # ======================================

    checks["Certifications"] = (
        "certification" in text or
        "certificate" in text
    )

    if checks["Certifications"]:
        score += 10
    else:
        suggestions.append(
            "Add Certifications."
        )

    # ======================================
    # Resume Length (5)
    # ======================================

    words = len(resume_text.split())

    if words < 150:

        checks["Good Resume Length"] = False

        suggestions.append(
            "Resume is too short. Add more project details and skills."
        )

    elif words > 600:

        checks["Good Resume Length"] = False

        suggestions.append(
            "Resume is too long. Keep it within 1-2 pages."
        )

    else:

        checks["Good Resume Length"] = True
        score += 5

    # ======================================
    # Formatting (5)
    # ======================================

    checks["Proper Formatting"] = "\n" in resume_text

    if checks["Proper Formatting"]:
        score += 5
    else:
        suggestions.append(
            "Improve resume formatting."
        )

    # ======================================
    # ATS Breakdown
    # ======================================

    breakdown = {
        "Skill Match": skill_score,
        "Contact Information": 10 if checks["Contact Information"] else 0,
        "Education": 10 if checks["Education"] else 0,
        "Experience": 10 if checks["Experience"] else 0,
        "Projects": 10 if checks["Projects"] else 0,
        "Certifications": 10 if checks["Certifications"] else 0,
        "Resume Length": 5 if checks["Good Resume Length"] else 0,
        "Formatting": 5 if checks["Proper Formatting"] else 0
    }

    score = min(score, 100)

    return (
    score,
    suggestions,
    checks,
    breakdown,
    words
)