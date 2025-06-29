from google import genai
from google.genai import types

def ask(prompt: str) -> str:
    client = genai.Client(api_key="")
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        ),
    ]
    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=-1),
        response_mime_type="text/plain",
    )
    response = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=contents,
        config=config,
    ):
        response += chunk.text
    return response


if __name__ == "__main__":
    prompt = "What is the capital of France?"
    response = ask(prompt)
    print("Response:", response)