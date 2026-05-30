import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


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
    generate_content(client, messages, args.verbose)


def generate_content(
    client: genai.Client, messages: list[types.Content], verbose: bool = False
) -> None:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
    )
    if response.usage_metadata is None:
        raise RuntimeError("Failed API call: usage_metadata not found.")

    if verbose:
        prompt_token_count = response.usage_metadata.prompt_token_count
        candidates_token_count = response.usage_metadata.candidates_token_count

        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidates_token_count}")

    print(f"Response: {response.text}")


if __name__ == "__main__":
    main()
