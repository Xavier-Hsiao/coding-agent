from config import MAX_CHARS
import os


def get_file_contents(working_directory: str, file_path: str) -> str:
    try:
        # check the file is within the working directory
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_file: bool = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )
        if not valid_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # check if the file is a real file
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # read the file up to 10,000 characters and return its content
        with open(target_file, "r", encoding="utf-8") as reader:
            file_content_string = reader.read(MAX_CHARS)
            # add the message if the content exceeds the char limit
            if reader.read(1):
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        return file_content_string

    except Exception as e:
        return f"Error: {e}"
