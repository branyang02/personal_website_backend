from openai import OpenAI

def get_word_details(word):
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant designed to output JSON.",
            },
            {"role": "user", "content": f"Give me the language of origin, definition, and example usage for the word '{word}' in the format: {{'word': '{word}', 'language_of_origin': '...', 'definition': '...', 'example_usage': '...'}}."},
        ],
    )
        
    return eval(response.choices[0].message.content)