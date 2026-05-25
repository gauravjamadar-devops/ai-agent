import os
from dotenv import load_dotenv
from google import genai

# Load API key
# comment
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Use a valid model name from list_models output
response = client.models.generate_content(
            model="models/gemini-2.5-flash",
                contents="Hello Gemini, introduce yourself in one line."
                )

print(response.text)

