import torch
from transformers import pipeline

def load_model(model_path="meta-llama/Meta-Llama-3-8B-Instruct"):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    pipe = pipeline(
        "text-generation",
        model=model_path,
        model_kwargs={"torch_dtype": torch.float16} if torch.cuda.is_available() else {},
        device=device,
    )
    return pipe
