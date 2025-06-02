from transformers import pipeline

class IA:
    def __init__(self, modelo_ai: str = "distilbert"):
        """
        Inicializa o pipeline de IA local
        """
        self.available_models = {
            "distilbert": "distilbert-base-uncased",
            "tiny-llama": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            "mistral": "mistralai/Mistral-7B-Instruct-v0.1",
        }

        self.set_model(modelo_ai)

    def set_model(self, modelo_ai: str):
        if modelo_ai not in self.available_models:
            raise ValueError(f"Modelo não suportado. Escolha entre {list(self.available_models.keys())}")
        model_name = self.available_models[modelo_ai]

        try:
            self.pipe = pipeline("text-generation", model=model_name)
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
            self.pipe = None

    def process(self, prompt: str) -> str:
        if self.pipe is None:
            return "Modelo não carregado."
        result = self.pipe(prompt, max_length=100, do_sample=True)[0]["generated_text"]
        return result
