import os

def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        absolute_path = os.path.abspath(full_path)
        working_path = os.path.abspath(working_directory)
        path_exists = os.path.exists(os.path.dirname(absolute_path))
        if not absolute_path.startswith(working_path + os.sep):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not path_exists:
            os.makedirs(os.path.dirname(absolute_path))
        with open(absolute_path, "w") as f:
            f.write(content)
        return f'Sucessfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error encountered: {e}"