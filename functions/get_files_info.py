import os

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        absolute_path = os.path.abspath(directory)
        working_directory_contents = os.listdir(working_directory)
        if absolute_path not in working_directory_contents:
            return f'Error: Cannot list {directory} as it is outside the permitted working directory'
        if not os.path.isdir(absolute_path):
            return f'Error: {directory} is not a directory'
        directory_info = "Result for current directory:\n"
        for file in working_directory_contents:
            file_path = os.path.join(full_path, file)
            file_size = os.path.getsize(full_path)
            is_dir = os.path.isdir(file_path)
            directory_info += f"- {file}: file_size={file_size} bytes, is_dir={is_dir}\n"
        directory_info = directory_info[:-1]
        return directory_info
    except Exception as e:
        return f"Error encountered: {e}"

