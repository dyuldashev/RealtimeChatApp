import torch
from transformers import AutoTokenizer
from unsloth import FastLanguageModel

def load_fine_tuned_model(load_dir="fine_tuned_llama_4bit"):
    """
    Load the fine-tuned LLaMA-3 model and tokenizer.

    Args:
        load_dir (str): Path to the directory containing the fine-tuned model and tokenizer.

    Returns:
        model: The loaded fine-tuned LLaMA-3 model.
        tokenizer: The corresponding tokenizer.
    """
    print(f"🔄 Loading tokenizer from {load_dir}...")
    tokenizer = AutoTokenizer.from_pretrained(load_dir)

    print("🔄 Loading base model (Unsloth LLaMA-3-8B in 4-bit mode)...")
    model, _ = FastLanguageModel.from_pretrained(
        model_name="unsloth/llama-3-8b-bnb-4bit",  # Base model
        max_seq_length=2048,
        dtype=None,
        load_in_4bit=True,
    )

    # Load fine-tuned adapter weights
    model_path = f"{load_dir}/adapter_model.bin"
    print(f"🔄 Loading fine-tuned adapter weights from {model_path}...")
    model.load_state_dict(torch.load(model_path, map_location="cpu"))

    print("✅ Model and tokenizer loaded successfully!")
    return model, tokenizer
