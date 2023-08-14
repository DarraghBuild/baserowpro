import requests

from django.conf import settings


def make_llama_chat_completion_request(
    question,
    system_role="You are a helpful assistant.",
    max_tokens=128
):
    url = f"{settings.BASEROW_LLAMA_API_URL}/v1/chat/completions"
    response = requests.post(
        url,
        json={
            "max_tokens": max_tokens,
            "messages": [
                {
                    "content": system_role,
                    "role": "system"
                },
                {
                    "content": question,
                    "role": "user"
                }
            ]
        },
        headers={
            "Content-type": "application/json"
        }
    )

    return response.json()["choices"][0]["message"]["content"]
