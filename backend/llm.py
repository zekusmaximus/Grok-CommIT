import os
from dotenv import load_dotenv
# from openai import OpenAI

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        # self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        
        # Load Primer
        try:
            with open("backend/primer.md", "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
        except FileNotFoundError:
            self.system_prompt = "You are the CommIT Guide."

    async def generate_response(self, messages: list) -> str:
        if not self.api_key:
            return "I am the CommIT Guide. Please configure your OPENAI_API_KEY to enable my full cognitive faculties."
        
        # Prepend system prompt
        full_messages = [{"role": "system", "content": self.system_prompt}] + messages
        
        # Placeholder for actual API call
        # response = self.client.chat.completions.create(
        #     model="gpt-4",
        #     messages=full_messages
        # )
        # return response.choices[0].message.content
        
        return "This is a simulated response from the Cognitive Engine. (LLM Integration Pending)"
