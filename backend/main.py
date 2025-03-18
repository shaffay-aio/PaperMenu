from backend.processing import encode_image, json_validator, convert_to_dataframe
from backend.model import prompt_template, model

def vlm(image_stream, file_stream):

    image_url = f"data:image/jpeg;base64, {encode_image(image_stream)}"
    
    prompt    = prompt_template(image_url)
    response  = model(prompt)

    parsed    = json_validator(response)
    dataframe = convert_to_dataframe(parsed)

    return dataframe

