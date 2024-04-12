from openai import OpenAI
from pathlib import Path
from pyston import PystonClient, File
import asyncio

client = OpenAI()


def get_word_details(word):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant designed to output JSON.",
            },
            {
                "role": "user",
                "content": f"Give me the language of origin, definition, and example usage for the word '{word}' in the format: {{'word': '{word}', 'language_of_origin': '...', 'definition': '...', 'example_usage': '...'}}.",
            },
        ],
    )

    return eval(response.choices[0].message.content)


def get_audio(text):
    """Converts text to speech using OpenAI's API and returns the file path."""
    response = client.audio.speech.create(
        model="tts-1", voice="alloy", input=text, response_format="mp3"
    )
    print(text)
    return response


def run_c_code_sync(code):
    result = None

    async def main_loop():
        nonlocal result
        client = PystonClient()
        output = await client.execute("c", [File(code)])
        result = output

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main_loop())
    finally:
        loop.close()

    result = result.raw_json
    print("-------------------")
    print(result)
    print("-------------------")

    if result["compile"]["code"] != 0:
        raise Exception(result["compile"]["stderr"])
    if result["run"]["code"] != 0:
        raise Exception(result["run"]["stderr"])

    return result["run"]["stdout"]
