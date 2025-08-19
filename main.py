import argparse
from data import load_text
from utils import save_result, list_ranked_results, load_weights_from_file
from model import load_model
from explanation import result_explanation
from inference import run_single_similarity, run_batch_similarity

DEFAULT_SECTION_WEIGHTS = {
    "Experience & Achievements": 0.2,
    "Skills & Competencies": 0.2,
    "Culture Fit": 0.2,
    "Personal Traits": 0.2,
    "Education": 0.2
}

def parse_arguments():
    parser = argparse.ArgumentParser(description="Resume vs Job Description Similarity Calculator")

    # Basic parameter 
    parser.add_argument("--jd", required=True, help="Job Description file (PDF or TXT)")

    # Resume (single or batch)
    parser.add_argument("--cv", help="Resume file (PDF or TXT)")
    parser.add_argument("--cv_folder", help="Folder containing multiple resume files (PDF/TXT)")

    # Text chunking & embedding model setting
    parser.add_argument("--model_id", type=str, default="sentence-transformers/all-MiniLM-L6-v2", help="Model ID for embedding")
    parser.add_argument("--llm_model", type=str, default="meta-llama/Meta-Llama-3-8B-Instruct", help="LLM model path or ID")

    # Record & Search history and comparison results
    parser.add_argument("--records", type=str, help="The records of previous matching results")
    parser.add_argument("--list", action="store_true", help="List and view similarity results")
    parser.add_argument("--filter_jd", type=str, help="Filter results by specific JD filename")
    parser.add_argument("--sort", action="store_true", help="Sort results by similarity score")
    parser.add_argument("--top_k", type=int, help="Only show top K results")

    # score weights
    parser.add_argument("--weight_config", type=str, help="YAML file with custom section weights")

    return parser.parse_args()

def main():
    args = parse_arguments()
    
    llm_pipe = load_model(model_path=args.llm_model)

    if args.weight_config:
        SECTION_WEIGHTS = load_weights_from_file(args.weight_config)
    else:
        SECTION_WEIGHTS = DEFAULT_SECTION_WEIGHTS

    RESULTS_FILE = args.records if args.records else 'results.csv'
    
    if args.list:
        list_ranked_results(
                jd_name=args.filter_jd, 
                result_file=RESULTS_FILE, 
                sort=args.sort,
                top_k=args.top_k
        )
        return
   
    if args.cv_folder:
        print("Running in batch mode...")
        results = run_batch_similarity(
            jd_path=args.jd,
            cv_input=args.cv_folder,
            SECTION_WEIGHTS=SECTION_WEIGHTS,
            model_id=args.model_id,
            llm_model=args.llm_model,
            pipe=llm_pipe
        )

        for r in results:
            print(f"{r['Resume']} - Score: {r['Similarity Score']}")
            section_scores = {k.replace(" Score", ""): r[k] for k in r if k.endswith(" Score")}
            save_result(r['JD'], r['Resume'], r['Similarity Score'], section_scores, RESULTS_FILE)

    elif args.cv:
        print("Running in single resume mode...")
        final_score, section_scores = run_single_similarity(
            jd_path=args.jd,
            cv_path=args.cv,
            SECTION_WEIGHTS=SECTION_WEIGHTS,
            model_id=args.model_id,
            llm_model=args.llm_model,
            pipe=llm_pipe
        )
        print(final_score)
        print(f"Final Similarity Score: {final_score}")
        for sec, val in section_scores.items():
            print(f"  - {sec}: {round(val, 4)}")

        save_result(args.jd, args.cv, final_score, section_scores, RESULTS_FILE)


        jd_text = load_text(args.jd)
        cv_text = load_text(args.cv)

        explanation_prompt = result_explanation(cv_text, jd_text)
        output = llm_pipe(explanation_prompt, max_new_tokens=1024)[0]["generated_text"][-1]["content"]
            
        print("\n Explanation:\n" + output.strip())

    else:
        print("Please provide either --cv or --cv_folder.")

if __name__ == "__main__":
    main()
