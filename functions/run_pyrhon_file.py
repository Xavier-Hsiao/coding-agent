import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute the specified python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to execute the specified python file, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Option arguments provided to execute the specified python file.",
            ),
        },
        required=["file_path"],
    ),
)


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_file: str = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file: bool = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith("py"):
            return f'Error: "{file_path}" is not a Python file'

        # prepare the subprocess to run
        command: list[str] = ["python", target_file]
        if args is not None:
            command.extend(args)

        result = subprocess.run(
            command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30
        )

        # build the output string
        output = ""
        if result.returncode != 0:
            output += "Process exited with code X\n"

        if len(result.stdout) == 0 and len(result.stderr) == 0:
            output += "No output produced"
        else:
            output += f"STDOUT: {result.stdout}"
            output += f"STDERR: {result.stderr}"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
