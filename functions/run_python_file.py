import os, subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_path = os.path.abspath(working_directory)
        if not full_path.startswith(working_path + os.sep):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: File "{file_path}" not found.'
        if not full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        cmd = ["python", full_path] + args
        run_file = subprocess.run(cmd, capture_output=True, timeout=30, cwd=os.path.dirname(full_path))
        if  not run_file.stdout:
            return "No output produced"
        run_info = f"STDOUT: {run_file.stdout}\n"
        run_info += f"STDERR: {run_file.stderr}\n"
        if run_file.returncode != 0:
            run_info += f"Process exited with code {run_file.returncode}"
        return run_info
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file and prints its output, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the pyton file in the working directory where it is run"
            ),
        },
    ),
)