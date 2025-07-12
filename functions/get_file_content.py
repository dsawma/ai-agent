import os
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_working_file = os.path.abspath(working_directory)
    if file_path and file_path != "":
        target_file = os.path.abspath(os.path.join(working_directory, file_path))
    else:
        return f'Error: File is empty or None'
    if not target_file.startswith(abs_working_file):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        MAX_CHARS = 10000
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) == MAX_CHARS and f.read(1) != "":
                return file_content_string + f'[...File "{file_path}" truncated at 10000 characters]'
            return file_content_string
    except Exception as e:
        return f"Error: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)