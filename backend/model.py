import os
from openai import OpenAI

def prompt_template(image_url):

    # output format json
    # necessary fields in output
    # any additional modifier/option fields
    sys_prompt = """
    You have to extract all the data from the menu in the JSON format.
    Donot write anything from yourself.
    """

    message = [
        {
            "role": "user",
            "content": 
            [
                { "type": "text", "text": sys_prompt},
                { "type": "image_url", "image_url": image_url},
            ],
        },
    ]

    return message

def model(prompt):
    
    client = OpenAI(api_key=os.getenv("QWEN_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

    response = client.chat.completions.create(
    model = "qwen-vl-max", response_format = {'type':'json_object'}, messages=prompt
    )

    return response.choices[0].message.content