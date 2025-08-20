# Resume Matcher with LLM & Embedding
This resume matcher helps HR professionals and recruiters efficiently identify candidates who best align with a given job description. By combining semantic understanding and AI-powered analysis, it goes beyond keyword matching to evaluate true fit.

## ⚙️ How It Works
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

## 🔍 Features
- Supports **PDF** and **TXT** file formats
- Upload one or multiple resumes to match against a single job description
  - **One resume:**  user can get the similarity score with detailed explanation
  - **Multiple resumes:** user can receive ranked similarity scores (no explanation for batch)
- Custom section weighting
- Explains the match using a language model
- Automatically records results to results.csv for persistent matching history and reusability

## Implementation
### CLI
#### Basic Arguments

| Argument           | Description |
|--------------------|-------------|
| `--jd`             | Path to **Job Description** file (PDF or TXT) |
| `--cv`             | Path to a **single Resume** file (PDF or TXT) |
| `--cv_folder`      | Path to a **folder** containing multiple resumes (PDF/TXT) |
| `--model_id`       | Embedding model (default: `sentence-transformers/all-MiniLM-L6-v2`) |
| `--llm_model`      | LLM for explanation (default: `meta-llama/Meta-Llama-3-8B-Instruct`) |
| `--records`        | Path to record `.csv` file to log or view results |
| `--list`           | List existing records (used with `--records`) |
| `--filter_jd`      | Filter record by JD filename |
| `--sort`           | Sort similarity scores in descending order |
| `--top_k`          | Show top K results from record |
| `--weight_config`  | YAML file with custom section weights |
#### Example
* **Match a Single Resume**

`python main.py --jd data/jd.txt --cv data/resume.pdf`

* **Match a Folder of Resumes (Batch Mode)**

`python main.py --jd data/jd.txt --cv_folder data/resumes/`

* **Use Custom Weighting (YAML)**

python main.py --jd data/jd.txt --cv data/resume.pdf --weight_config config/weights.yaml`

* **Record and View Results**
```
# Run and record
python main.py --jd data/jd.txt --cv_folder data/resumes/ --records results.csv

# View all results
python main.py --records results.csv --list

# Filter by JD and sort by score
python main.py --records results.csv --list --filter_jd jd.txt --sort --top_k 5
```

## 🧾 Outcome Illustration
* **Single Resume Matching**
<p align="center">
<img width="500" height="400" alt="image" src="https://github.com/user-attachments/assets/9c950765-605f-49da-9210-4783c5543bad" />
</p>

* **Batch Resume Ranking**
<p align="center">
<img width="1353" height="205" alt="image" src="https://github.com/user-attachments/assets/b8db9d36-9df0-42d3-a50e-0e4c7e5f4e89" />
</p>


