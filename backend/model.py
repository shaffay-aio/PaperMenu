import os
from openai import OpenAI

sys_prompt = """You have to extract all the data from the menu in the JSON format.
Do not write anything from yourself. If any information in below given format is missing keep it empty.
Do not break the output structure. You have to extract only food categories, items, prices and descriptions.

Output Format:
[
    {'category' : '', 'item': '', 'price': , 'description': ''}, 
]
"""

def prompt_template(image_url):

    message = [
        {
            "role": "user",
            "content": 
            [
                { "type": "text", "text": sys_prompt},
                { "type": "image_url", "image_url": {"url" : image_url}},
            ],
        },
    ]

    return message

def modelQwen(prompt):
    
    client = OpenAI(api_key=os.getenv("QWEN_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

    response = client.chat.completions.create(
    model = "qwen-vl-max", response_format = {'type':'json_object'}, 
    messages=prompt, temperature=0.0
    )

    return response.choices[0].message.content

def modelGemini(prompt):

    client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"), base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

    response = client.chat.completions.create(
    model = "gemini-2.0-flash-lite", response_format = {'type':'json_object'}, messages=prompt
    )

    return response.choices[0].message.content