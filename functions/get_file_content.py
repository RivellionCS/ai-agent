import os
MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    try:
        absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        absolute_working_directory = os.path.abspath(working_directory)
        working_directory_contents = os.listdir(absolute_working_directory)
        file_in_working_directory = False
        for file in working_directory_contents:
            if file_path.startswith(file):
                file_in_working_directory = True
        if not file_in_working_directory:
            return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
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