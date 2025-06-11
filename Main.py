from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from collections import Counter
import pdfplumber
import textstat
import shutil
import os
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_pdf(pdf_file):
    try:
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(e)
        return ""

def get_keyword_score(text):
    technical_keywords = ["python", "java", "javascript", "sql", "html", "css", "react", "angular", "vue",
        "node.js", "mongodb", "postgresql", "mysql", "git", "docker", "kubernetes",
        "aws", "azure", "gcp", "machine learning", "data analysis", "artificial intelligence",
        "deep learning", "tensorflow", "pytorch", "pandas", "numpy", "scikit-learn"
    ]
    soft_skills = ["leadership", "teamwork", "communication", "problem solving", "analytical",
        "project management", "collaboration", "mentoring", "strategic planning",
        "critical thinking", "adaptability", "innovation", "creativity"
    ]
    all_keywords = technical_keywords + soft_skills
    words = re.findall(r"\b\w+\b", text.lower())
    word_freq = Counter(words)
    keyword_matches = sum([word_freq.get(keyword, 0) for keyword in all_keywords])
    unique_keywords_found = sum([1 for keyword in all_keywords if keyword in words])
    base_score = min(keyword_matches * 0.8, 20)
    diversity_bonus = min(unique_keywords_found * 0.5, 10)
    return min(base_score + diversity_bonus, 30)

def get_readability_score(text):
    try:
        if len(text.strip()) < 50:
            return 0
        flesch_score = textstat.flesch_reading_ease(text)
        if 60 <= flesch_score <= 70:
            return 25
        elif 50 <= flesch_score < 60 or 70 < flesch_score <= 80:
            return 20
        elif 40 <= flesch_score < 50 or 80 < flesch_score <= 90:
            return 15
        else:
            return 10
    except:
        return 15

def check_sections(text):
    essential_sections = {
        "contact": ["email", "phone", "linkedin", "contact"],
        "experience": ["experience", "work", "employment", "career", "professional"],
        "education": ["education", "degree", "university", "college", "school"],
        "skills": ["skills", "technologies", "proficient", "expertise", "competencies"],
        "projects": ["projects", "portfolio", "achievements", "accomplishments"]
    }
    text_lower = text.lower()
    sections_found = 0
    section_details = {}
    for section, keywords in essential_sections.items():
        found = any(keyword in text_lower for keyword in keywords)
        section_details[section] = found
        if found:
            sections_found += 1
    score = (sections_found / len(essential_sections)) * 25
    return score, section_details

def get_length_score(text):
    word_count = len(text.split())
    if 300 <= word_count <= 800:
        return 20
    elif 200 <= word_count < 300 or 800 < word_count <= 1200:
        return 15
    elif 100 <= word_count < 200 or 1200 < word_count <= 1500:
        return 10
    else:
        return 5

def generate_suggestions(keyword_score, readability_score, section_score, section_details, length_score, word_count):
    suggestions = []
    if keyword_score < 15:
        suggestions.append({
            "type": "warning",
            "title": "⚠️ Low Keyword Density",
            "message": "Consider adding more relevant technical skills and industry keywords."
        })
    elif keyword_score < 25:
        suggestions.append({
            "type": "info",
            "title": "💡 Keyword Optimization",
            "message": "Good keyword usage! Add more specific technical or soft skills for improvement."
        })
    if readability_score < 15:
        suggestions.append({
            "type": "warning",
            "title": "📖 Readability Concerns",
            "message": "Try using clearer language and formatting."
        })
    missing_sections = [sec for sec, present in section_details.items() if not present]
    if missing_sections:
        suggestions.append({
            "type": "error",
            "title": "📋 Missing Sections",
            "message": f"Add these important sections: {', '.join(missing_sections).title()}"
        })
    if length_score < 15:
        if word_count < 300:
            suggestions.append({
                "type": "info",
                "title": "📏 Resume Too Short",
                "message": "Add more detail about experiences and skills."
            })
        elif word_count > 1200:
            suggestions.append({
                "type": "info",
                "title": "📏 Resume Too Long",
                "message": "Shorten it by focusing on the most relevant content."
            })
    return suggestions

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        text = extract_text_from_pdf(temp_path)
        keyword_score = get_keyword_score(text)
        readability_score = get_readability_score(text)
        section_score, section_details = check_sections(text)
        length_score = get_length_score(text)
        total_score = keyword_score + readability_score + section_score + length_score
        suggestions = generate_suggestions(
            keyword_score, readability_score, section_score, section_details, length_score, len(text.split())
        )

        return {
            "keyword_score": keyword_score,
            "readability_score": readability_score,
            "section_score": section_score,
            "length_score": length_score,
            "total_score": total_score,
            "suggestions": suggestions
        }

    finally:
        os.remove(temp_path)
