# Resume Matcher with LLM & Embedding
This resume matcher helps HR professionals and recruiters efficiently identify candidates who best align with a given job description. By combining semantic understanding and AI-powered analysis, it goes beyond keyword matching to evaluate true fit.

### ⚙️ How It Works
The tool leverages a large language model (LLM) to analyze both the job description and resumes. It summarizes each document into five essential dimensions:
- **Experience & Achievements**
- **Skills & Competencies**
- **Culture Fit**
- **Personal Traits**
- **Education**

These structured summaries are then converted into embeddings. The tool calculates similarity scores across each of the five dimensions to provide a context-aware comparison between the job description and resumes.

$\quad$ <img width="700" height="500" alt="image" src="https://github.com/user-attachments/assets/02c7e39e-e42b-4bed-b9d5-5eb1442d6095" />


### 🔍 Features
- Supports **PDF** and **TXT** file formats
- Upload one or multiple resumes to match against a single job description
  - **One resume:**  user can get the similarity score with detailed explanation
  - **Multiple resumes:** user can receive ranked similarity scores (no explanation for batch)
- Custom section weighting
- Explains the match using a language model
- Automatically records results to results.csv for persistent matching history and reusability

