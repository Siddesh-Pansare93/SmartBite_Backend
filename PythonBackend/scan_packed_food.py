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


system_message = """
You are an expert at structured data extraction. You will be given an image of packed food and you must convert it into the given structue by extracting the ingredients and the nutritional facts, for nutritional facts the amount should be equal to the amount of food the the user is consuming, if not mentioned then consider the whole packet (per serve). Also the values of in the nutrition_fact should be in grams, if given in miligrams then convert it to grams. Use g for grams unit
You have also been provided the user_profile, based on the medical history and allergies and other useful info, find out whether it is good for the user to eat it, and give a feedback and its advantages or disagvantages.
In the feedback, warn the user if the food is not good for them due to their allergies or medical history if such ingredients are present in the food.
You have also been provided with the user's diet, based on the user's diet and give you final thoughts about whether the user should eat it
"""


class food_info_extraction_format(BaseModel):
    nutritional_facts: list[str, str]
    ingredients: list[str]
    feedback: str
    final_thoughts: str

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_data(image_path, user_prompt, user_profile, user_diet):
    base64_image = encode_image(image_path)

    completion = client.beta.chat.completions.parse(
        model=Model,
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        # "text": "This is maggie noodles, I am gonna eat all of this",
                        "text": f"{user_prompt} {user_profile} {user_diet}",
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
    print(data)

    with open("response.txt", "w") as f:
        f.write(data)
    
    return data

def clean_data(data):    
    parsed_data = json.loads(data)
    nutritional_facts = parsed_data.get("nutritional_facts", [])
    ingredients = parsed_data.get("ingredients", [])
    feedback = parsed_data.get("feedback", [])
    final_thoughts = parsed_data.get("final_thoughts", [])

    # print(nutritional_facts)
    # print(ingredients)
    # print(feedback)
    # print(final_thoughts)

    # Process the list into a dictionary
    nutritional_facts_dict = {}
    for fact in nutritional_facts:
        fact = fact.lstrip("-").strip()
        key, value = fact.split(": ")
        # value = value.replace("g", "").strip()
        nutritional_facts_dict[key] = value

    # Convert to JSON
    nutritional_facts_json = json.dumps(nutritional_facts_dict, indent=2)
    return nutritional_facts_json, ingredients, feedback, final_thoughts

def scan(image_path, user_prompt, user_profile, user_diet):
    data = get_data(image_path, user_prompt, user_profile, user_diet)
    # print(data)
    nutritional_facts_json, ingredients, feedback, final_thoughts = clean_data(data)
    return [nutritional_facts_json, ingredients, feedback, final_thoughts]
    


if __name__ == "__main__":
    image_path = input("Enter the path to the image: ")
    user_prompt = input("Enter the user prompt: ")
    # nutritional_facts_json, ingredients = scan(image_path, user_prompt)
    # print(nutritional_facts_json)
    # print(ingredients)

    # example
    user_profile = {
        "Age": "20",
        "weight (kg)": "70",
        "Height (cm)": "170",
        "Gender": "Male",
        "Activity Level": "Moderately Active",
        "Dietary Preferences": "Vegetarian",
        "Allergies": "None",
        "Taste Preferences": "Spicy",
        "Medical History": "None",
    }


    user_diet = {"nutrients":{"Calories":2500,"Proteins":80,"Carbohydrates":350,"Fats":70,"Sugar":50,"Sodium":2000,"Fiber":30,"Vitamin A":900,"Vitamin C":90,"Calcium":1000,"Iron":14,"Magnesium":400,"Potassium":3500,"Vitamin B12":2.4},"mealSuggestions":["Meal 1: Tofu stir-fry with mixed vegetables (broccoli, bell peppers, and carrots) served with brown rice. Seasoned with soy sauce and sesame oil.","Meal 2: Whole grain pasta with marinara sauce, lentils, and spinach topped with nutritional yeast.","Meal 3: Smoothie with banana, spinach, almond milk, and a scoop of plant-based protein powder.","Meal 4: Quinoa salad with chickpeas, cherry tomatoes, cucumber, avocado, and a lemon-tahini dressing.","Meal 5: Vegetable curry with sweet potatoes and served with basmati rice and side of mixed greens salad with vinaigrette."]}



    result = scan(image_path, user_prompt, user_profile, user_diet)
    print(result[0])
    print(result[1])
    print(result[2])
    print(result[3])