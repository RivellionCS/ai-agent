import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function
MAX_STEPS = 20

def main():
    if len(sys.argv) < 2:
        print('Error: program was called incorrectly\nUsage: python3 main.py "Text Prompt"')
        sys.exit(1)
    else:
        system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
        available_functions =  types.Tool(
            function_declarations=[
                schema_get_files_info,
                schema_get_file_content,
                schema_run_python_file,
                schema_write_file,
            ]
        )
        args = []
        for arg in sys.argv[1:]:
            if not arg.startswith("--"):
                args.append(arg)
        user_prompt = " ".join(args)
        verbose = "--verbose" in sys.argv
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]
        for i in range(MAX_STEPS):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash-001", 
                    contents=messages,
                    config=types.GenerateContentConfig(
                        tools=[available_functions], system_instruction=system_prompt
                        )
                    )
                response_candidate = response.candidates
                has_any_function_call = False
                function_calls = []
                for candidate in response_candidate:
                    messages.append(candidate.content)

                    if candidate.content and candidate.content.parts:
                        for part in candidate.content.parts:
                            if part.function_call is not None:
                                has_any_function_call = True
                                function_calls.append(part.function_call)

                if response.text and not has_any_function_call:
                    print(response.text)
                    break

                function_list = []
                for function_call in function_calls:
                    called_function = call_function(function_call, verbose)
                    function_list.append(called_function.parts[0])
                usage = response.usage_metadata


                if function_list:
                    messages.append(types.Content(role="user", parts=function_list))

                

                if verbose:
                    print(f"User prompt: {user_prompt}")
                    print(f"Prompt tokens: {usage.prompt_token_count}")
                    print(f"Response tokens: {usage.candidates_token_count}")
            except Exception as e:
                print(f"Error: {e}")
                break



if __name__ == "__main__":
    main()
