from google.genai import types

import os

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write contents to a specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write contents into, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the specified file.",
            ),
        },
        required=["file_path", "content"],
    ),
)


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file: bool = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # make sure that all parent directories of target_file_path exist
        # otherwise we create them on the fly
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w", encoding="utf-8") as file_writer:
            file_writer.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"
