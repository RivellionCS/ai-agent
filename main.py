import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    if len(sys.argv) < 2:
        print('Error: program was called incorrectly\nUsage: python3 main.py "Text Prompt"')
        sys.exit(1)
    else:
        user_prompt = sys.argv[1]
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents=messages,
            )
        usage = response.usage_metadata
        print(response.text)
        if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {usage.prompt_token_count}")
            print(f"Response tokens: {usage.candidates_token_count}")



if __name__ == "__main__":
    main()
