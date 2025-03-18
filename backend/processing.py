import json
import io, base64
import pandas as pd
from PIL import Image

def encode_image(image_path):
    
    # Open the image file
    with Image.open(image_path) as img:

        # Resize the image using high-quality downsampling
        img = img.resize((1000, 1000), Image.Resampling.LANCZOS)
        
        # Save the resized image to a byte buffer
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        
        # Encode the image to base64
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

def json_validator(response):

    try:
        parsed_json = json.loads(response.replace("```json","").strip("```").strip())
        print("Json loaded")
        return parsed_json

    except json.JSONDecodeError as e:
        print("Failed to decode JSON from the response:")
        print(response)
        raise e
    
def convert_to_dataframe(parsed_json):

    menu_list = []

    for category, items in parsed_json.items():
        if isinstance(items, dict):
            for item, price in items.items():
                description = item
                menu_list.append([category, item, price, description])
        else:
            menu_list.append([category, items, "", items])

    df = pd.DataFrame(menu_list, columns=["Category", "Item", "Price", "Description"])
    return df