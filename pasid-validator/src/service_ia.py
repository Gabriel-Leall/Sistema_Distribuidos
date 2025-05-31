from ollama import ChatResponse, Client

class IA:
    def __init__(self):
        self.models = {
            "llama3.2": "llama3.2",
            "deep-seek": "DeepSeek-R1"
        }

        self.model = self.models["llama3.2"] 

        self.client = Client(
            host="http://ollama:11434"
        )

    def ask(self, prompt: str) -> str:
        ia_response:ChatResponse = self.client.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return ia_response.message.content