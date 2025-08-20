# 📄 Resume Matcher with LLM & Embedding
This resume matcher helps HR professionals and recruiters efficiently identify candidates who best align with a given job description. By combining semantic understanding and AI-powered analysis, it goes beyond keyword matching to evaluate true fit.

## ⚙️ How It Works
The tool leverages a large language model (LLM) to analyze both the job description and resumes. It summarizes each document into five essential dimensions:
- **Experience & Achievements**
- **Skills & Competencies**
- **Culture Fit**
- **Personal Traits**
- **Education**

These structured summaries are then converted into embeddings. The tool calculates similarity scores across each of the five dimensions to provide a context-aware comparison between the job description and resumes.

## 🔍 Features
- Supports **PDF** and **TXT** file formats
- Upload one or multiple resumes to match against a single job description
  - **One resume:**  user can get the similarity score with detailed explanation
  - **Multiple resumes:** user can receive ranked similarity scores (no explanation for batch)
- Custom section weighting
- Explains the match using a language model
- Automatically records results to results.csv for persistent matching history and reusability

## 🛠️ Implementation
### 🖥️ CLI
#### 📝 Basic Arguments

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
#### ⚡ Example
* **Match a Single Resume**

  `python main.py --jd data/jd.txt --cv data/resume.pdf`

* **Match a Folder of Resumes (Batch Mode)**

  `python main.py --jd data/jd.txt --cv_folder data/resumes/`

* **Use Custom Weighting (YAML)**

  `python main.py --jd data/jd.txt --cv data/resume.pdf --weight_config config/weights.yaml`

* **Record and View Results**
  ```
  # Run and record
  python main.py --jd data/jd.txt --cv_folder data/resumes/ --records results.csv
  
  # View all results
  python main.py --records results.csv --list
  
  # Filter by JD and sort by score
  python main.py --records results.csv --list --filter_jd jd.txt --sort --top_k 5
  ```

### 🌐 API
This system provides two main API endpoints for calculating similarity between resumes and job descriptions (JD).

#### `/compare/single`  
Compare a single resume against a job description and get a detailed explanation.

* **Method**
`POST`

* **Form Data**

  | Parameter       | Type        | Required | Description                          |
  |-----------------|-------------|----------|------------------------------------|
  | `jd_file`       | File        | Yes      | Job Description file (PDF or TXT)  |
  | `cv_file`       | File        | Yes      | Resume file (PDF or TXT)            |
  | `weights_file`  | File        | No       | Optional YAML file for custom weights |
  | `model_id`      | String      | No       | Embedding model ID (default: `sentence-transformers/all-MiniLM-L6-v2`) |

* **Sample Response (JSON)**
  * **Single**
    ```json
    {
      "resume": "resume1.pdf",
      "jd": "jd1.txt",
      "similarity_score": 0.8235,
      "section_scores": {
        "Experience & Achievements": 0.81,
        "Skills & Competencies": 0.84,
        "Culture Fit": 0.79,
        "Personal Traits": 0.85,
        "Education": 0.80
      },
      "explanation": "The resume aligns well with the job requirements, especially in skills and experience..."
    }
    ```
  * **Batch**
    ```
    {
      "results": [
        {
          "JD": "jd1.txt",
          "Resume": "resume1.pdf",
          "Similarity Score": 0.8235
        },
        {
          "JD": "jd1.txt",
          "Resume": "resume2.pdf",
          "Similarity Score": 0.7482
        }
      ]
    }
    ```

## 🎛️ Demo
This demo app allows you to upload a Job Description and one or multiple Resumes for similarity matching. You can adjust the importance (weights) of five resume sections before running the matching.

### 🚀 Launch
`python app.py`

### 🧑‍💻 How to Use:
1. Upload your Job Description file
2. Upload one or multiple resume files
3. Adjust the section weights (ensure they roughly sum to 1.0)
4. Click "Run Matching"  
5. View similarity scores and explanations for single mode or a ranked table for batch mode

<p align="center">
<img width="700" height="500" alt="image" src="https://github.com/user-attachments/assets/02c7e39e-e42b-4bed-b9d5-5eb1442d6095" />
</p>

### 🧾 Outcome Illustration
* **Single Resume Matching**
<p align="center">
<img width="500" height="400" alt="image" src="https://github.com/user-attachments/assets/9c950765-605f-49da-9210-4783c5543bad" />
</p>

* **Batch Resume Ranking**
<p align="center">
<img width="1353" height="205" alt="image" src="https://github.com/user-attachments/assets/b8db9d36-9df0-42d3-a50e-0e4c7e5f4e89" />
</p>


