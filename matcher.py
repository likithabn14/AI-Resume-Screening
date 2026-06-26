import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ======================================================
# MASTER SKILL LIST
# ======================================================

SKILLS = [

    # Programming
    "python","java","c","c++","c#","r","sql",

    # Web
    "html","css","javascript","react","node js",
    "flask","django",

    # Data Science
    "data science",
    "data analysis",
    "data analytics",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "statistics",
    "data visualization",
    "data cleaning",
    "eda",
    "exploratory data analysis",

    # Libraries
    "numpy",
    "pandas",
    "matplotlib",
    "seaborn",
    "scikit learn",
    "tensorflow",
    "keras",
    "pytorch",

    # BI
    "excel",
    "power bi",
    "tableau",

    # Database
    "mysql",
    "postgresql",
    "mongodb",
    "nosql",

    # Cloud
    "aws",
    "azure",
    "gcp",

    # Big Data
    "spark",
    "hadoop",

    # DevOps
    "docker",
    "kubernetes",

    # Version Control
    "git",
    "github",

    # OS
    "linux",

    # Agile
    "jira",
    "agile",

    # Soft Skills
    "communication",
    "problem solving",
    "teamwork",
    "leadership"
]

# ======================================================
# SKILL WEIGHTS
# ======================================================

SKILL_WEIGHTS = {

    # Programming
    "python": 10,
    "sql": 10,
    "r": 8,

    # Data Science
    "machine learning": 8,
    "data analysis": 8,
    "data analytics": 8,
    "data science": 8,

    # Libraries
    "pandas": 8,
    "numpy": 8,
    "matplotlib": 7,
    "seaborn": 7,
    "scikit learn": 7,

    # BI
    "power bi": 7,
    "tableau": 7,
    "excel": 7,

    # Statistics
    "statistics": 6,
    "eda": 6,
    "data cleaning": 6,
    "data visualization": 6,

    # Databases
    "mysql": 5,
    "postgresql": 5,
    "mongodb": 5,

    # Cloud
    "aws": 4,
    "azure": 4,
    "gcp": 4,

    # Tools
    "git": 3,
    "github": 3,

    # Soft Skills
    "communication": 2,
    "teamwork": 2,
    "leadership": 2,
    "problem solving": 2
}

# ======================================================
# SKILL SYNONYMS
# ======================================================

SYNONYMS = {
    "artificial intelligence": ["ai"],
    "machine learning": ["ml"],
    "data analysis": ["data analytics"],
    "power bi": ["powerbi"],
    "scikit learn": ["scikit-learn", "sklearn"],
    "javascript": ["js"],
    "numpy": ["np"],
    "structured query language": ["sql"],
    "exploratory data analysis": ["eda"]
}

# ======================================================
# Normalize
# ======================================================

def clean(text):

    text = text.lower()
    text = re.sub(r"[^a-z0-9+# ]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ======================================================
# Main Function
# ======================================================

def analyze_resume(job_description, resume_text):

    jd = clean(job_description)
    resume = clean(resume_text)

    # Search the whole resume (including projects)
    project_text = resume

    # ----------------------------------------
    # Extract Required Skills from JD
    # ----------------------------------------

    required_skills = []

    for skill in SKILLS:

        skill_text = clean(skill)

        if skill_text in jd:
            required_skills.append(skill)

    required_skills = list(set(required_skills))

    # ----------------------------------------
    # Match Skills
    # ----------------------------------------

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        skill_text = clean(skill)

        found = False

        # Exact Match
        if skill_text in resume:
            found = True

        # Match in Projects
        elif skill_text in project_text:
            found = True

        # Synonym Match
        elif skill_text in SYNONYMS:

            for synonym in SYNONYMS[skill_text]:

                if clean(synonym) in resume:
                    found = True
                    break

        if found:
            matched_skills.append(skill.title())
        else:
            missing_skills.append(skill.title())

    # ----------------------------------------
    # Weighted Skill Match
    # ----------------------------------------

    matched_weight = 0
    required_weight = 0

    for skill in required_skills:

        weight = SKILL_WEIGHTS.get(skill.lower(), 5)

        required_weight += weight

        if skill.title() in matched_skills:
            matched_weight += weight

    if required_weight == 0:
        skill_match = 50

    else:
        skill_match = (matched_weight / required_weight) * 100

    # ----------------------------------------
    # Cosine Similarity
    # ----------------------------------------

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(
        [job_description, resume_text]
    )

    cosine = cosine_similarity(
        vectors[0],
        vectors[1]
    )[0][0] * 100

    # ----------------------------------------
    # Final Resume Match
    # ----------------------------------------

    match_percentage = round(
        (0.80 * skill_match) +
        (0.20 * cosine),
        2
    )

    # ----------------------------------------
    # Recommendation
    # ----------------------------------------

    if match_percentage >= 85:
        recommendation = "🌟 Excellent Match"

    elif match_percentage >= 70:
        recommendation = "✅ Good Match"

    elif match_percentage >= 50:
        recommendation = "⚠️ Average Match"

    else:
        recommendation = "❌ Poor Match"

    return (
        match_percentage,
        matched_skills,
        missing_skills,
        recommendation
    )