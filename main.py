import os, sys
from dotenv import load_dotenv
from google import genai

def main():
    if len(sys.argv) < 2:
        print('Error: program was called incorrectly\nUsage: python3 main.py "Text Prompt"')
        sys.exit(1)
    else:
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents=sys.argv[1],
            )
        usage = response.usage_metadata
        print(response.text)
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")



if __name__ == "__main__":
    main()
