from pydantic import BaseModel
import base64
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
import json


key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=key)
Model = "gpt-4o-mini"

class food_info_extraction_format(BaseModel):
    nutritional_facts: list[str, str]
    ingredients: list[str]

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_data(image_path, user_prompt):
    base64_image = encode_image(image_path)

    completion = client.beta.chat.completions.parse(
        model=Model,
        messages=[
            {
                "role": "system",
                "content": "You are an expert at structured data extraction. You will be given an image of packed food and you must convert it into the given structue by extracting the ingredients and the nutritional facts, for nutritional facts the amount should be equal to the amount of food the the user is consuming, if not mentioned then consider the whole packet (per serve). Also the values of in the nutrition_fact should be in float and in grams, if given in miligrams then convert it to grams"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        # "text": "This is maggie noodles, I am gonna eat all of this",
                        "text": user_prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        response_format=food_info_extraction_format,


    )
    data = completion.choices[0].message.content
    # print(data)

    with open("response.txt", "w") as f:
        f.write(data)
    
    return data

def clean_data(data):    
    parsed_data = json.loads(data)
    nutritional_facts = parsed_data.get("nutritional_facts", [])
    ingredients = parsed_data.get("ingredients", [])

    # Process the list into a dictionary
    nutritional_facts_dict = {}
    for fact in nutritional_facts:
        fact = fact.lstrip("-").strip()
        key, value = fact.split(": ")
        value = value.replace("g", "").strip()
        nutritional_facts_dict[key] = float(value)
        # nutritional_facts_dict[key] = value

    # Convert to JSON
    nutritional_facts_json = json.dumps(nutritional_facts_dict, indent=2)
    return nutritional_facts_json, ingredients

def scan(image_path, user_prompt):
    data = get_data(image_path, user_prompt)
    nutritional_facts_json, ingredients = clean_data(data)
    return nutritional_facts_json, ingredients
    


if __name__ == "__main__":
    image_path = input("Enter the path to the image: ")
    user_prompt = input("Enter the user prompt: ")
    nutritional_facts_json, ingredients = scan(image_path, user_prompt)
    print(nutritional_facts_json)
    print(ingredients)