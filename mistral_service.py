import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key = api_key)

def ask_mistral(
        question: str,
        response_format = { "type": "text" },
        model = "mistral-large-latest"
    ):

    chat_response = client.chat.complete(
        model = model,
        messages = [{
                "role": "user",
                "content": question,
            }],
        response_format = response_format
    )

    return chat_response.choices[0].message.content