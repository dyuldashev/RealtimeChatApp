import torch
from .model_loader import load_fine_tuned_model

def translator(text, target_language="English"):
    """
    Translate a given text into the specified target language using LLaMA-3.

    Args:
        text (str): The input text to be translated.
        target_language (str): The target language for translation (default: "English").

    Returns:
        str: Translated text in the target language.
    """

    alpaca_prompt = """
    Below is an instruction that describes a task. Write a response that appropriately completes the request.

    ### Instruction:
    {instruction}

    ### Input:
    {input}

    ### Response:
    """
    instruction = f"""
    You are a professional translator. Your task is to accurately translate the given text into {target_language}.

    Instructions:
    1. Translate the text from the source language to {target_language}.
    2. Maintain the original meaning and tone.
    3. Use appropriate {target_language} grammar and vocabulary.
    4. If you encounter an ambiguous or unfamiliar word, provide the most likely translation based on context.
    5. Output only the translation, without any additional comments.

    Now, please translate the following text into {target_language}:
    """

    formatted_prompt = alpaca_prompt.format(instruction=instruction, input=text)

    model, tokenizer = load_fine_tuned_model()

    inputs = tokenizer(
        formatted_prompt,
        return_tensors="pt",
        padding=True,
        truncation=True
    ).to("cpu")

    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=200)

    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return translation.strip()
