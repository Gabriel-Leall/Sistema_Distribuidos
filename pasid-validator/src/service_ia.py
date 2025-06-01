from ollama import Client
from typing import Dict, Optional
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class IA:
    def __init__(self, model_name: str = "llama3.2"):
        """
        Inicializa o serviço de IA com os modelos disponíveis
        
        Args:
            model_name: Nome do modelo a ser usado (default: "llama3.2")
        """
        self.available_models = {
            "llama3.2": "llama3.2",
            "deep-seek": "DeepSeek-R1"
        }
        
        self.set_model(model_name)
        self.client = Client(host="http://ollama:11434")
        
        # Inicialização do modelo local (se necessário)
        self.tokenizer = None
        self.local_model = None

    def set_model(self, model_name: str) -> None:
        """Define o modelo a ser usado"""
        if model_name not in self.available_models:
            raise ValueError(f"Modelo não disponível. Opções: {list(self.available_models.keys())}")
        self.model = self.available_models[model_name]

    def load_local_model(self, model_path: str) -> None:
        """Carrega um modelo local (opcional)"""
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.local_model = AutoModelForCausalLM.from_pretrained(model_path)

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

    def process_text_locally(self, prompt: str) -> Optional[str]:
        """
        Processa texto localmente (se modelo carregado)
        
        Args:
            prompt: Texto de entrada
            
        Returns:
            Resposta do modelo ou None se não estiver configurado
        """
        if not self.local_model or not self.tokenizer:
            print("Modelo local não carregado")
            return None
            
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.local_model.device)
            with torch.no_grad():
                outputs = self.local_model.generate(**inputs, max_new_tokens=50)
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            print(f"Erro no processamento local: {str(e)}")
            return None

    def process(self, prompt: str, use_local: bool = False) -> str:
        """
        Método principal para processamento de texto
        
        Args:
            prompt: Texto de entrada
            use_local: Se True, usa modelo local (se disponível)
            
        Returns:
            Resposta do modelo
        """
        if use_local and self.local_model:
            return self.process_text_locally(prompt) or self.ask_ollama(prompt)
        return self.ask_ollama(prompt)

if __name__ == "__main__":
    # Exemplo de uso
    ia = IA(model_name="llama3.2")
    
    # Teste com Ollama
    prompt = "Explique o que é balanceamento de carga em sistemas distribuídos."
    resposta = ia.process(prompt)
    print("Resposta Ollama:", resposta)
    
    # Teste com modelo local (se configurado)
    # ia.load_local_model("caminho/para/modelo")
    # resposta_local = ia.process(prompt, use_local=True)
    # print("Resposta Local:", resposta_local)