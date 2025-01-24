import base64
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os

key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=key)

Model = "gpt-4o-mini"


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image
image_path = "images/ss.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)


system = """
Analyze the given image of the packed food item and extract the contents of the nutritional facts and also the ingredients as the amount of the food the user eats,
if not provided then consider the whole pack.
Generate a JSON object "nutritional_facts" with the fields of all the nutritional facts and their quantity as their values:
Generate a python list "ingredients" of ingredients
Return only the JSON object "nutritional_facts" and the list "ingredients", nothing else.
"""




response = client.chat.completions.create(
    model=Model,
    messages=[
        {
            "role": "system",
            "content": system,
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "This is maggie noodles, I am gonna eat all of this",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    ],


)


print("\n\n")
print(response.choices[0].message.content)
print(type(response.choices[0].message.content))

# print("\n\n")
# print(response.choices[0].message)
# print(type(response.choices[0].message))



# save response to a file
with open("response.json", "w") as f:
    f.write(response.choices[0].message.content)
    f.close()
