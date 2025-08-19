import os
import argparse
from pathlib import Path
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--tmpdir", type=str, default=None, help="Temporary directory for Gradio uploads")
args, _ = parser.parse_known_args()

tmpdir = args.tmpdir or os.environ.get("GRADIO_TMPDIR") or "./gradio_tmp"
Path(tmpdir).mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"] = tmpdir
print(f"Using TMPDIR: {tmpdir}")

import gradio as gr
from inference import run_single_similarity, run_batch_similarity
from data import load_text
from model import load_model
from explanation import result_explanation

pipe = load_model()

def gradio_inference(jd_file, cv_files, top_k,
                     w_exp, w_skills, w_culture, w_traits, w_edu):
    jd_path = jd_file.name
    jd_text = load_text(jd_path)

    weights = {
        "Experience & Achievements": w_exp,
        "Skills & Competencies": w_skills,
        "Culture Fit": w_culture,
        "Personal Traits": w_traits,
        "Education": w_edu
    }

    total_weight = sum(weights.values())
    if abs(total_weight - 1.0) > 0.1:
        warning = f"⚠️ Warning: Total weight is {total_weight:.2f}, please adjust to sum ~1.0"
    else:
        warning = ""

    if len(cv_files) == 1:
        cv_path = cv_files[0].name
        cv_text = load_text(cv_path)

        final_score, section_scores = run_single_similarity(
            jd_path=jd_path,
            cv_path=cv_path,
            SECTION_WEIGHTS=weights,
            model_id="sentence-transformers/all-MiniLM-L6-v2",
            pipe=pipe
        )

        prompt = result_explanation(cv_text, jd_text)
        explanation = pipe(prompt, max_new_tokens=1024)[0]["generated_text"]
        explanation_text = explanation[2]['content'].strip() if isinstance(explanation, list) else explanation

        section_text = "\n".join([f"- {k}: {round(v, 4)}" for k, v in section_scores.items()])
        return round(final_score, 4), f"{warning}\n\nSection Scores:\n{section_text}\n\nExplanation:\n{explanation_text}", None

    else:
        cv_paths = [f.name for f in cv_files]

        results = run_batch_similarity(
            jd_path=jd_path,
            cv_input=cv_paths,
            SECTION_WEIGHTS=weights,
            model_id="sentence-transformers/all-MiniLM-L6-v2",
            pipe=pipe
        )

        results_sorted = sorted(results, key=lambda x: x["Similarity Score"], reverse=True)
        for idx, row in enumerate(results_sorted):
            row["Rank"] = idx + 1

        top_results = results_sorted[:top_k]
        df = pd.DataFrame(top_results)
        return None, None, df

with gr.Blocks() as demo:
    gr.Markdown("## 📄 Resume ⇄ Job Description Matching Tool (LLM Summary + Adjustable Weights)")

    with gr.Row():
        jd_input = gr.File(label="Upload Job Description (PDF or TXT)", file_types=[".pdf", ".txt"])
        cv_input = gr.File(label="Upload Resumes (PDF or TXT)", file_types=[".pdf", ".txt"], file_count="multiple")

    gr.Markdown("### 🎯 Section Weights (Total should roughly sum to 1.0)")

    with gr.Row():
        w_exp = gr.Number(label="Experience & Achievements", value=0.2, step=0.01)
        w_skills = gr.Number(label="Skills & Competencies", value=0.2, step=0.01)
        w_culture = gr.Number(label="Culture Fit", value=0.2, step=0.01)
        w_traits = gr.Number(label="Personal Traits", value=0.2, step=0.01)
        w_edu = gr.Number(label="Education", value=0.2, step=0.01)

    top_n_slider = gr.Slider(minimum=1, maximum=20, step=1, value=5, label="Top N Results (Batch Mode Only)")

    score_output = gr.Number(label="Similarity Score (Single Mode Only)")
    explanation_output = gr.Textbox(label="Section Scores + Explanation", lines=15)
    dataframe_output = gr.Dataframe(label="Batch Similarity Results", interactive=False)

    run_button = gr.Button("Run Matching")

    run_button.click(
        fn=gradio_inference,
        inputs=[
            jd_input, cv_input, top_n_slider,
            w_exp, w_skills, w_culture, w_traits, w_edu
        ],
        outputs=[score_output, explanation_output, dataframe_output]
    )

if __name__ == "__main__":
    #demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
    demo.launch(server_name="0.0.0.0", share=False)
