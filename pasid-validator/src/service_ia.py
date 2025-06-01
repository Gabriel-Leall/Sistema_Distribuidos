from ollama import Client


class IA:
    def __init__(self, nome_modelo: str = "llama3.2"):
        """
        Inicializa o serviço de IA com os modelos disponíveis
        
        Args:
            nome_modelo: Nome do modelo a ser usado (default: "llama3.2")
        """
        self.available_models = {
            "llama3.2": "llama3.2",
            "deep-seek": "DeepSeek-R1"
        }

        self.set_model(nome_modelo)
        self.client = Client(host="http://ollama:11434")

    def set_model(self, nome_modelo: str) -> None:
        """Define o modelo a ser usado"""
        if nome_modelo not in self.available_models:
            raise ValueError(f"Modelo não disponível. Opções: {list(self.available_models.keys())}")
        self.model = self.available_models[nome_modelo]

    def ask_ollama(self, prompt: str) -> str:
        """
        Envia prompt para o modelo via Ollama
        
        Args:
            prompt: Texto de entrada para o modelo
            
        Returns:
            Resposta do modelo
        """
        try:
            response = self.client.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response['message']['content']
        except Exception as e:
            print(f"Erro ao consultar Ollama: {str(e)}")
            return "Erro ao processar a requisição"

    def process(self, prompt: str) -> str:
        """
        Método principal para processamento de texto
        
        Args:
            prompt: Texto de entrada
            
        Returns:
            Resposta do modelo
        """
        return self.ask_ollama(prompt)


if __name__ == "__main__":
    # Exemplo de uso
    ia = IA(nome_modelo="llama3.2")

    prompt = "Explique o que é balanceamento de carga em sistemas distribuídos."
    resposta = ia.process(prompt)
    print("Resposta Ollama:", resposta)
