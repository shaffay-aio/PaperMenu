import os
from openai import OpenAI
from fastapi import HTTPException
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()

sys_prompt = """You have to extract all the data from the menu in the provided JSON format.
Strictly follow the instructions given below:
- Do not write anything from yourself. If any information in below given format is missing keep it empty.
- Do not break the output structure. You have to extract only food categories, items, prices and descriptions.
- Where no information for a specific entity is found, it should add "" rather than null.
- If item with different prices exist, make separate entries for them.
- Auto correct any spelling mistakes. 
- One entry should be made for a combo. If multiple items exist in combo, add all its items as one item. Be careful while picking category name for it.
- Where no categories are found but items exist, keep their category empty.

Output Format:
[
    {'category' : <str: name of food category>, 
    'item': <str: name of food item>, 
    'price': <str: price of food item>,  
    'description': <str: description of food item>}, 
]
"""

def prompt_template(image_url):

    message = [
        {
            "role": "developer",
            "content": sys_prompt
        },
        {
            "role": "user",
            "content": 
            [
                { "type": "image_url", "image_url": {"url" : image_url}},
            ],
        },
    ]

    return message

def modelQwen(prompt):
    
    try:
        client = OpenAI(api_key=os.getenv("QWEN_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

        response = client.chat.completions.create(
        model = "qwen-vl-max", response_format = {'type':'json_object'}, 
        messages=prompt, temperature=0.0
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Bad Gateway. Model response error. {e}")
    
    return response.choices[0].message.content

def modelGemini(prompt):

    try:
        client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"), base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

        response = client.chat.completions.create(
        model = "gemini-2.0-flash-lite", 
        response_format = {'type':'json_schema'}, 
        messages=prompt, 
        temperature=0.0, 
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Bad Gateway. Model response error. {e}")

    return response.choices[0].message.content