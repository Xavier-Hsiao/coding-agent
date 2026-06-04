from ast import arg
from typing import Callable

from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_contents import get_file_contents, schema_get_file_contents
from functions.write_file import schema_write_file, write_file
from functions.run_pyrhon_file import run_python_file, schema_run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_contents,
        schema_write_file,
        schema_run_python_file,
    ],
)


def call_function(
    function_call: types.FunctionCall, verbose: bool = False
) -> types.Content:
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    print(f" - Calling function: {function_call.name}")

    # determine which functions to call
    functions_map: dict[str, Callable[..., str]] = {
        "get_files_info": get_files_info,
        "get_file_contents": get_file_contents,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    function_name = function_call.name or ""
    if function_name not in functions_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"

    function_result: str = functions_map[function_name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name, response={"result": function_result}
            )
        ],
    )
