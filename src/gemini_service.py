import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self, model: str = None):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = model or os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    def summarize(self, text: str, system_instruction: str = None) -> str:
        """
        Summarizes the provided text using Gemini.
        """
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
            max_output_tokens=2048,
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=text,
            config=config
        )

        if response.text:
            return response.text
        
        return "Error: No response text from Gemini."

if __name__ == "__main__":
    # Quick test
    service = GeminiService()
    print(service.summarize("Hello! How are you? Speak like a pirate."))
