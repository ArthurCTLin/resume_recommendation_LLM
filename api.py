from fastapi import FastAPI, UploadFile, File, Form
from typing import List
import os
import shutil
from inference import run_single_similarity, run_batch_similarity
from data import load_text
from utils import save_result
from explanation import result_explanation
from model import load_model
import yaml

app = FastAPI()

# Load LLM model once
llm_pipe = load_model()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Default section weights (you can customize this)
DEFAULT_SECTION_WEIGHTS = {
    "Experience & Achievements": 0.2,
    "Skills & Competencies": 0.2,
    "Culture Fit": 0.2,
    "Personal Traits": 0.2,
    "Education": 0.2
}

def load_weights_from_upload(file: UploadFile):
    if file is None:
        return None
    content = file.file.read().decode("utf-8")
    return yaml.safe_load(content)

@app.post('/compare/single')
async def compare_single(
    jd_file: UploadFile = File(...),
    cv_file: UploadFile = File(...),
    weights_file: UploadFile = File(None),
    model_id: str = Form("sentence-transformers/all-MiniLM-L6-v2")
):
    jd_path = os.path.join(UPLOAD_DIR, jd_file.filename)
    cv_path = os.path.join(UPLOAD_DIR, cv_file.filename)

    with open(jd_path, "wb") as f:
        shutil.copyfileobj(jd_file.file, f)

    with open(cv_path, "wb") as f:
        shutil.copyfileobj(cv_file.file, f)

    section_weights = load_weights_from_upload(weights_file) or DEFAULT_SECTION_WEIGHTS
    
    # Run similarity
    final_score, section_scores = run_single_similarity(
        jd_path=jd_path,
        cv_path=cv_path,
        SECTION_WEIGHTS=section_weights,
        model_id=model_id,
        pipe=llm_pipe
    )

    # Explanation
    jd_text = load_text(jd_path)
    cv_text = load_text(cv_path)
    prompt = result_explanation(cv_text, jd_text)
    explanation = llm_pipe(prompt, max_new_tokens=1024)

    return {
        "resume": os.path.basename(cv_path),
        "jd": os.path.basename(jd_path),
        "similarity_score": round(final_score, 4),
        "section_scores": {k: round(v, 4) for k, v in section_scores.items()},
        "explanation": explanation[0]["generated_text"][2]['content'].strip()
    }

@app.post("/compare/batch/")
async def compare_batch(
    jd_file: UploadFile = File(...),
    resumes: List[UploadFile] = File(...),
    model_id: str = Form("sentence-transformers/all-MiniLM-L6-v2")
):
    jd_path = os.path.join(UPLOAD_DIR, jd_file.filename)
    with open(jd_path, "wb") as f:
        shutil.copyfileobj(jd_file.file, f)

    cv_folder = os.path.join(UPLOAD_DIR, "batch_cvs")
    os.makedirs(cv_folder, exist_ok=True)

    for file in resumes:
        dest_path = os.path.join(cv_folder, file.filename)
        with open(dest_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

    section_weights = load_weights_from_upload(weights_file) or DEFAULT_SECTION_WEIGHTS

    results = run_batch_similarity(
        jd_path=jd_path,
        cv_input=cv_folder,
        SECTION_WEIGHTS=section_weights,
        model_id=model_id,
        pipe=llm_pipe
    )

    return {"results": results}
