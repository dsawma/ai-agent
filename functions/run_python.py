import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path):
    abs_working_file = os.path.abspath(working_directory)
    if file_path and file_path != "":
        target_file = os.path.abspath(os.path.join(working_directory, file_path))
    else:
        return f'Error: File is empty or None'
    if not target_file.startswith(abs_working_file):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File "{file_path}" not found.'
    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run(["python", target_file], timeout= 30, stdout=subprocess.PIPE, stderr= subprocess.PIPE, cwd=working_directory )
        ret =f'STDOUT:{result.stdout.decode()}\nSTDERR:{result.stderr.decode()}'
        if result.returncode != 0:
            ret += f"\nProcess exited with code {result.returncode}"
        if result.stdout.decode() == "" and result.stderr.decode() == "":
            return "No output produced"
        return ret

    except Exception as e:
        return f"Error: executing Python file: {e}"



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
