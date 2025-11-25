import os
from google.genai import types
MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    try:
        absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        absolute_working_directory = os.path.abspath(working_directory)
        if not absolute_file_path.startswith(absolute_working_directory + os.sep):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(absolute_file_path):
            return(f'Error: File not found or is not a regular file: "{file_path}"')
        
        with open(absolute_file_path, "r") as f:
            file_text = f.read()
            if len(file_text) > MAX_CHARS:
                file_text = file_text[:MAX_CHARS + 1]
                return f'{file_text}\n[...File "{file_path}" truncated at {MAX_CHARS} characters.]'
            else:
                return f'{file_text}'
    except Exception as e:
        return f"Error encountered: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads the content of the file in the specific directory and truncates it to {MAX_CHARS} if total characters is greater than {MAX_CHARS}, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file in the working directory if not valid or not provided an error will occur"
            ),
        },
    ),
)