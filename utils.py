import pandas as pd
from datetime import datetime
import os 
import yaml

def save_result(jd_file, cv_file, weighted_score, section_scores, RESULTS_FILE="results.csv"):
    record = {
        "JD": os.path.basename(jd_file),
        "Resume": os.path.basename(cv_file),
        "Similarity Score": float(weighted_score),
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    for sec, val in section_scores.items():
        record[f"{sec} Score"] = round(val, 4)

    if os.path.exists(RESULTS_FILE):
        df = pd.read_csv(RESULTS_FILE)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    else:
        df = pd.DataFrame([record])

    df.to_csv(RESULTS_FILE, index=False)
    print(f"Result saved to {RESULTS_FILE}")

def list_ranked_results(jd_name=None, results_file='results.csv', sort=False, top_k=None):
    if not os.path.exists(results_file):
        print("No results found.")
        return

    df = pd.read_csv(results_file)

    if jd_name:
        df = df[df["JD"] == jd_name]

    if sort:
        df = df.sort_values(by="Similarity Score", ascending=False)

    if top_k:
        df = df.head(top_k)
    
    print(df.to_string(index=False))

def load_weights_from_file(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)
