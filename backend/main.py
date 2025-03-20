from backend.embeddings import merge
from backend.model import prompt_template, model
from backend.processing import encode_image, json_validator, convert_to_dataframe

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def vlm(image_stream):

    # process image
    encoded   = encode_image(image_stream)
    image_url = f"data:image/jpeg;base64, {encoded}"
    
    # build prompt and perform inference
    prompt    = prompt_template(image_url)
    response  = model(prompt)

    # process output
    parsed    = json_validator(response)
    dataframe = convert_to_dataframe(parsed)

    return dataframe
            

def pipeline(image_stream, file_stream):
    
    #dataframe = vlm(image_stream)
    print("menu extracted")

    file = pd.read_excel(file_stream, sheet_name=None)
    merged    = merge(file['items'], file['items'])
    print("files marged")
    pass