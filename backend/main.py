import io
import pandas as pd

from backend.embeddings import merge
from backend.model import prompt_template, model
from backend.processing import encode_image, json_validator, convert_to_dataframe

from dotenv import load_dotenv
load_dotenv()

from backend.utils.logging import setup_logger
logger = setup_logger(__name__)

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
    
    # extract menu
    dataframe = vlm(image_stream)
    logger.info(f"Image processed successfully. {dataframe['Category Name'].nunique()} categories & {dataframe['Item Name'].nunique()} items extracted.")

    # merge non-existent items with scraped file
    file = pd.read_excel(file_stream, sheet_name=None)
    file['items'], missing_items = merge(dataframe, file['items'])
    logger.info(f"Scraped and OCR files merged successfully. {missing_items['Item Name'].nunique()} additional items added.")

    # convert to aio format
    #logger.info("File converted to AIO format.")

    # apply super menu
    #logger.info("Super Menu modifier/option filling added.")

    # convert excel file to byte stream object
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for key in file.keys():
            file[key].to_excel(writer, sheet_name=key, index=False)            
    output.seek(0)

    return output