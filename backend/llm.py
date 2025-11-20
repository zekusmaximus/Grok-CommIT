import os
import google.generativeai as genai
from openai import AsyncOpenAI
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.system_prompt = "You are the CommIT Guide."
        
        # Load Primer
        try:
            with open("backend/primer.md", "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
        except FileNotFoundError:
            print("Warning: primer.md not found in backend/. Using default.")

        # Initialize Clients
        self.openai_client = None
        self.groq_client = None
        self.gemini_model = None

        if self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.openai_client = AsyncOpenAI(api_key=api_key)
        
        elif self.provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if api_key:
                self.groq_client = AsyncGroq(api_key=api_key)
        
        elif self.provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                # System instructions are passed at model creation in newer Gemini versions
                self.gemini_model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=self.system_prompt
                )

        elif self.provider == "ollama":
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
            self.openai_client = AsyncOpenAI(
                base_url=base_url,
                api_key="ollama" # Required but unused
            )

    async def generate_response(self, messages: list) -> str:
        try:
            if self.provider == "openai":
                if not self.openai_client:
                    return "Error: OpenAI API Key not configured."
                
                full_messages = [{"role": "system", "content": self.system_prompt}] + messages
                response = await self.openai_client.chat.completions.create(
                    model="gpt-4-turbo", # Or gpt-4o
                    messages=full_messages
                )
                return response.choices[0].message.content

            elif self.provider == "groq":
                if not self.groq_client:
                    return "Error: Groq API Key not configured."
                
                full_messages = [{"role": "system", "content": self.system_prompt}] + messages
                response = await self.groq_client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=full_messages
                )
                return response.choices[0].message.content

            elif self.provider == "ollama":
                if not self.openai_client:
                    return "Error: Ollama client failed to initialize."
                
                model = os.getenv("OLLAMA_MODEL", "llama3")
                full_messages = [{"role": "system", "content": self.system_prompt}] + messages
                response = await self.openai_client.chat.completions.create(
                    model=model,
                    messages=full_messages
                )
                return response.choices[0].message.content

            elif self.provider == "gemini":
                if not self.gemini_model:
                    return "Error: Gemini API Key not configured."
                
                # Gemini handles history differently (ChatSession), but for single turn/stateless API:
                # We need to convert standard messages to Gemini format
                gemini_history = []
                for msg in messages:
                    role = "user" if msg["role"] == "user" else "model"
                    gemini_history.append({"role": role, "parts": [msg["content"]]})
                
                # Generate
                response = await self.gemini_model.generate_content_async(gemini_history)
                return response.text

            else:
                return f"Error: Unsupported provider '{self.provider}'."

        except Exception as e:
            return f"Error communicating with {self.provider}: {str(e)}"
