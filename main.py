import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
args = sys.argv[1:]
user_prompt = " ".join(args)
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
response = client.models.generate_content(model ="gemini-2.0-flash-001", contents =messages)
print(response.text)
if "--verbose" in user_prompt:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")