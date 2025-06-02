import markovify

class IA:
    def __init__(self, modelo_ai: str = "markov"):
        """
        Inicializa um gerador de texto simples baseado em Markov
        """
        self.available_models = {
            "markov": "default"
        }

        self.set_model(modelo_ai)

    def set_model(self, modelo_ai: str):
        if modelo_ai not in self.available_models:
            raise ValueError(f"Modelo não suportado. Escolha entre {list(self.available_models.keys())}")
        
        # Exemplo de corpus simples para treinar
        corpus = """
        O rato roeu a roupa do rei de Roma. 
        A aranha arranha a rã. 
        A Rita levou a marmita. 
        O tempo perguntou pro tempo quanto tempo o tempo tem.
        """
        try:
            self.model = markovify.Text(corpus)
        except Exception as e:
            print(f"Erro ao inicializar modelo Markov: {e}")
            self.model = None

    def process(self, prompt: str) -> str:
        if self.model is None:
            return "Modelo não carregado."
        return self.model.make_sentence() or "Não consegui gerar uma resposta."

# Exemplo de uso:
# ia = IA()
# print(ia.process("teste"))
