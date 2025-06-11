# 📄 Resume Analyzer — AI-Based Resume Feedback Tool

This project provides a smart analysis of resumes to help job seekers optimize their Applicant Tracking System (ATS)-friendly resumes (ATF resumes). It scores your resume across key metrics such as keyword relevance, readability, section completeness, and length, and then generates tailored suggestions for improvement.

> ⚠️ **IMPORTANT:** Please upload an **ATF (Applicant Tracking Friendly)** resume in **PDF format** — not a graphical or overly stylized one. Use standard fonts, clear headings, and text-based content. Images, columns, and non-standard formatting may lead to inaccurate analysis or scoring.

---

## 🚀 Features

- ✅ **Keyword Matching**: Identifies use of technical skills & soft skills based on job relevance.
- ✅ **Readability Scoring**: Uses readability formulas to evaluate complexity and clarity.
- ✅ **Section Detection**: Checks for essential resume sections like Education, Projects, Skills, etc.
- ✅ **Length Check**: Assesses optimal word count.
- ✅ **Improvement Suggestions**: Personalized feedback and tips for resume enhancement.

---

## 📁 Project Structure

```
placement/
│
├── main.py                # Backend logic for resume analysis
├── index.html             # Frontend UI for file upload and result display
├── resume.pdf             # Sample input (for testing)
└── requirements.txt       # Python dependencies
```

---

## ⚙️ How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/jaipriyaa/ResumeAnalyser-ML.git
cd ResumeAnalyser-ML
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

**`requirements.txt`**
```txt
fastapi
uvicorn
pdfplumber
textstat
python-multipart
```

### 3. Start FastAPI Backend
```bash
uvicorn Main:app --reload
```

### 4. Open Frontend
Just open `index.html` in a browser.

---

## 📂 Uploading Your Resume

> Upload a **PDF resume that is ATF-compliant**:
> - Use **simple formatting**
> - Avoid **tables**, **columns**, or **images**
> - Use **text-based content**, not scanned images
> - Clearly label sections like `Education`, `Skills`, `Projects`, `Experience`

---

## 📊 Sample Output

Once analyzed, you’ll get:

- A score breakdown: `Keyword Score`, `Readability`, `Section Coverage`, `Length Score`, and `Total Score`
- Suggestions like:
  - 📖 *“Your resume may be too complex. Simplify your language.”*
  - 📋 *“Add a Skills section to highlight your technical expertise.”*

---

## 💡 Ideal Use Cases

- Resume screening feedback before applying
- Improving resumes for job portals
- HR or placement cell tools for resume evaluation

---

## 🤝 Contributing

Have ideas to improve the scoring or UI? Contributions are welcome! Submit a pull request or open an issue.

---

## 📜 License

MIT License — use it freely with attribution.
