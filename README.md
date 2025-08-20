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

<p align="center">
<img width="700" height="500" alt="image" src="https://github.com/user-attachments/assets/02c7e39e-e42b-4bed-b9d5-5eb1442d6095" />
</p>


### 🔍 Features
- Supports **PDF** and **TXT** file formats
- Upload one or multiple resumes to match against a single job description
  - **One resume:**  user can get the similarity score with detailed explanation
  - **Multiple resumes:** user can receive ranked similarity scores (no explanation for batch)
- Custom section weighting
- Explains the match using a language model
- Automatically records results to results.csv for persistent matching history and reusability

### 🧾 Outcome Illustration
* **Single Resume Matching**
<p align="center">
<img width="500" height="400" alt="image" src="https://github.com/user-attachments/assets/9c950765-605f-49da-9210-4783c5543bad" />
</p>

* **Batch Resume Ranking**
<p align="center">
<img width="1353" height="205" alt="image" src="https://github.com/user-attachments/assets/b8db9d36-9df0-42d3-a50e-0e4c7e5f4e89" />
</p>


