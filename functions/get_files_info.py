import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    """
    The directory will be treated as relative path within the working_directory.
    Limit the scope of directories and files that LLM can view.
    This prevent the LLM from performing any works outside the working_directory that we give.
    """
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(working_dir_abs, directory))

        # validate the path to the directory is within the working_directory
        valid_target_dir: bool = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # list files
        files_info = "\n"
        try:
            files: list[str] = os.listdir(target_dir)
            for file in files:
                file_name: str = file
                file_path = os.path.join(target_dir, file)
                file_size: int = os.path.getsize(file_path)
                files_info += f"- {file_name}: file_size={file_size} bytes, is_dir={os.path.isdir(file_path)}\n"
        except Exception as e:
            return f"Error: {e}"

        return f"Result for current directory: {files_info}"

    except Exception as e:
        return f"Error: calling os library functions failed: {e}"
