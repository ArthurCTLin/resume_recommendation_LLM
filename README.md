# Resume Matcher with LLM & Embedding

This tool allows you to:
- Upload a **Job Description** and **one or more Resumes**
- Adjust section weights like experience, skills, etc.
- Get **similarity scores** and a **LLM-generated explanation**

### Features
- Support PDF / TXT files
- Uses `sentence-transformers` and custom section weighting
- Explains the match using a language model

### Model Used
- **Embedding model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Summary and explanation model:** `meta-llama/Meta-Llama-3-8B-Instruct`
