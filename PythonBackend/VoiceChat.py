
import os
from groq import Groq
from openai import OpenAI
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)
# client = Groq(
#     api_key=os.environ.get("GROQ_API_KEY"),
# )


client = Groq()



def get_text(filename):
    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
          file=(filename, file.read()),
          model="whisper-large-v3-turbo",
          response_format="verbose_json",
        )
        return transcription.text






def run_full_turn(system_message, messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_message}] + messages,
    )
    message = response.choices[0].message
    messages.append(message)

    if message.content: print("Assistant:", message.content)

    return message

messages = []




system_message = """
You are an expert nutritionist. Help the user with their queries regarding their diet and the food they are eating.
Refuse to answer any questions that are not related to nutrition or health.
"""

messages = []



def get_response(messages, user):
    messages.append({"role": "user", "content": user})

    result = run_full_turn(system_message, messages)
    return result



def VoiceChat(filename, messages):
    text = get_text(filename)
    result = get_response(messages, text)
    return result




































