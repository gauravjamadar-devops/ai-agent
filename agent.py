import os
import subprocess
from dotenv import load_dotenv
from google import genai

class GeminiAgent:
    def __init__(self, model_name="models/gemini-2.5-flash", role="You are a helpful assistant."):
        load_dotenv()
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = model_name
        self.role = role
        self.history = []

    def ask(self, prompt: str) -> str:
        self.history.append(f"User: {prompt}")
        conversation = self.role + "\n" + "\n".join(self.history) + "\nAssistant:"

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=conversation
        )

        reply = response.text
        self.history.append(f"Assistant: {reply}")

        # Tool orchestration
        if "```python" in reply:
            code = self.extract_code(reply)
            if code:
                result = self.run_python(code)
                reply += f"\n\n[Python Execution Result]\n{result}"

        elif "search:" in reply.lower():
            query = self.extract_search(reply)
            result = self.run_search(query)
            reply += f"\n\n[Search Result]\n{result}"

        return reply

    def extract_code(self, text: str) -> str:
        import re
        matches = re.findall(r"```python(.*?)```", text, re.DOTALL)
        if matches:
            return matches[0].strip()
        return ""

    def run_python(self, code: str) -> str:
        try:
            result = subprocess.run(
                ["python", "-c", code],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            return str(e)

    def extract_search(self, text: str) -> str:
        # Simple heuristic: look for "search: query"
        import re
        match = re.search(r"search:\s*(.*)", text, re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def run_search(self, query: str) -> str:
        # Placeholder: you can integrate Bing, Google, or any API here
        return f"(Pretend search results for: {query})"
