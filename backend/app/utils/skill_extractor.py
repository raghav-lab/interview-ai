SKILLS = [
    "Python",
    "Java",
    "C++",
    "C",
    "JavaScript",
    "React",
    "Node.js",
    "FastAPI",
    "SQL",
    "PostgreSQL",
    "MongoDB",
    "HTML",
    "CSS",
    "Git",
    "Docker",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "Pandas",
    "NumPy"
]

def extract_skills(text: str):

    found_skills = []

    lower_text = text.lower()

    for skill in SKILLS:

        if skill.lower() in lower_text:

            found_skills.append(skill)

    return found_skills