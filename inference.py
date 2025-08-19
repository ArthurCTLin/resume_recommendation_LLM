import os 
from data import load_text 
from generate_summary_and_embedding import generate_summary_and_embedding
from cal_sim import compute_similarity

def run_single_similarity(jd_path, cv_path, SECTION_WEIGHTS, model_id="sentence-transformers/all-MiniLM-L6-v2", llm_model="meta-llama/Meta-Llama-3-8B-Instruct", pipe=None):
    
    jd_text = load_text(jd_path)
    cv_text = load_text(cv_path)
    
    jd_embeddings, _ = generate_summary_and_embedding(jd_text, text_type="job_description", model_id=model_id, llm_model=llm_model, pipe=pipe)
    cv_embeddings, _ = generate_summary_and_embedding(cv_text, text_type="resume", model_id=model_id, llm_model=llm_model, pipe=pipe)

    scores = compute_similarity(jd_embeddings, cv_embeddings)
    weighted_scores = sum(scores[k] * SECTION_WEIGHTS.get(k, 0) for k in scores)
    return round(float(weighted_scores), 4), scores

def run_batch_similarity(jd_path, cv_input, SECTION_WEIGHTS, model_id="sentence-transformers/all-MiniLM-L6-v2", llm_model="meta-ll    ama/Meta-Llama-3-8B-Instruct", pipe=None):
    
    jd_text = load_text(jd_path)
    jd_embeddings, _ = generate_summary_and_embedding(jd_text, text_type="job_description", model_id=model_id, llm_model=llm_model, pipe=pipe)
    
    if isinstance(cv_input, str):
        cv_paths = [
            os.path.join(cv_input, f)
            for f in os.listdir(cv_input)
            if os.path.isfile(os.path.join(cv_input, f)) and f.lower().endswith(('.pdf', '.txt'))
        ]
    elif isinstance(cv_input, list):
        cv_paths = cv_input 
    else:
        raise ValueError("cv_input must be path directory (str) or list of file paths (list[str])")
        
    results = []
    for full_cv_path in cv_paths:
        filename = os.path.basename(full_cv_path)

        try:
            cv_text = load_text(full_cv_path)
            cv_embeddings, _ = generate_summary_and_embedding(cv_text, text_type="resume", model_id=model_id, llm_model=llm_model, pipe=pipe)
            scores = compute_similarity(jd_embeddings, cv_embeddings)
            weighted_scores = sum(scores[k] * SECTION_WEIGHTS.get(k, 0) for k in scores)

            result = {
                "JD": os.path.basename(jd_path),
                "Resume": filename,
                "Similarity Score": round(float(weighted_scores), 4)
            }

            for sec, val in scores.items():
                result[f"{sec} Score"] = round(val, 4)

            results.append(result)

        except Exception as e:
            print(f"❌ Failed to process {filename}: {e}")

    return results
