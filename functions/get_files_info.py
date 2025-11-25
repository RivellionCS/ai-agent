import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        absolute_path = os.path.abspath(full_path)
        working_path = os.path.abspath(working_directory)
        working_directory_contents = os.listdir(working_path)
        directory_contents = os.listdir(absolute_path)
        directory_info = f"Result for '{directory}' directory:\n"
        if directory not in working_directory_contents and directory != ".":
            return f'{directory_info}   Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(absolute_path):
            return f'Error: "{directory}" is not a directory'
        if directory == ".":
            directory_info = "Result for current directory:\n"
        for file in directory_contents:
            file_path = os.path.join(full_path, file)
            file_size = os.path.getsize(full_path)
            is_dir = os.path.isdir(file_path)
            directory_info += f"- {file}: file_size={file_size} bytes, is_dir={is_dir}\n"
        directory_info = directory_info[:-1]
        return directory_info
    except Exception as e:
        return f"Error encountered: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

