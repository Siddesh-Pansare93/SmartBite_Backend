from openai import OpenAI
import datetime
from dotenv import load_dotenv
load_dotenv()
import os
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

Model = "gpt-4o-mini"

messages = []
system_message = """
You are an expert nutritionist. You have to help the user with the food he is currently eating, the user's profile data like the medical history and allergies and more have been provided,
you have to help the user with any queries regarding his plan and the food he is eating.
"""




def get_response(system_message, messages):
    response = client.chat.completions.create(
        model=Model,
        messages=[{"role": "system", "content": system_message}] + messages,
    )
    message = response.choices[0].message
    messages.append(message)

    if message.content: print("Assistant:", message.content)

    return message


def chat(messages, user):
    messages.append({"role": "user", "content": user})

    result = get_response(system_message, messages)


if __name__ == '__main__':
    get_response(system_message, messages)