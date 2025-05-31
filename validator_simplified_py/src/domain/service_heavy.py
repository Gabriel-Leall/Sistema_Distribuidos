from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Carrega o modelo DeepSeek (exemplo: deepseek-ai/deepseek-llm-7b-base)
model_name = "deepseek-ai/deepseek-llm-7b-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")

def process_text(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=20)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    # Exemplo de uso: simula uma requisição recebida
    prompt = "Explique o que é balanceamento de carga em sistemas distribuídos."
    resposta = process_text(prompt)
    print("Resposta IA:", resposta)
