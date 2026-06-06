import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    # handle env variables
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Gemimi API Key not found!")

    # handle argument parser
    parser = argparse.ArgumentParser(description="coding-agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # communicate with LLM
    # we use `messages` to handle conversation history
    client = genai.Client(api_key=api_key)
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    done = False
    for _ in range(20):
        done = generate_content(client, messages, args.verbose)
        if done:
            break
    if not done:
        print("The conversation exceeds the turn limits.")
        sys.exit(1)


def generate_content(
    client: genai.Client, messages: list[types.Content], verbose: bool = False
) -> bool:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, tools=[available_functions]
        ),
    )
    if response.usage_metadata is None:
        raise RuntimeError("Failed API call: usage_metadata not found.")

    if verbose:
        prompt_token_count = response.usage_metadata.prompt_token_count
        candidates_token_count = response.usage_metadata.candidates_token_count

        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidates_token_count}")

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    function_results = []
    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose)
            if not function_call_result.parts or len(function_call_result.parts) == 0:
                raise Exception("No valid function result from function call.")

            function_response = function_call_result.parts[0].function_response
            if not function_response:
                raise Exception("No valid function response from function call.")

            function_result = function_response.response
            if not function_result:
                raise Exception("No valid function result from function call.")

            function_results.append(function_call_result.parts[0])

            if verbose:
                print(f"-> {function_result}")

        messages.append(types.Content(role="user", parts=function_results))

        # we have function_calls in the model's response -> the conversation should continue
        return False

    print(f"Response: {response.text}")

    return True


if __name__ == "__main__":
    main()
