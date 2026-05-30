import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    """
    The directory will be treated as relative path within the working_directory.
    Limit the scope of directories and files that LLM can view.
    This prevent the LLM from performing any works outside the working_directory that we give.
    """
    # validate the path to the directory is within the working_directory
    try:
        working_dir_abs: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir: bool = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'

        return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f"Error: calling os library functions failed: {e}"
