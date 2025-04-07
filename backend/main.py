import pandas as pd

from backend.embeddings import merge
from backend.model import prompt_template, modelGemini, modelQwen
from backend.processing import encode_image, list_validator, convert_to_dataframe, additional_columns, convert_to_aio

from dotenv import load_dotenv
load_dotenv()

from backend.utils.logging import setup_logger
logger = setup_logger(__name__)

def vlm(image_stream):

    # process image
    encoded   = encode_image(image_stream)
    image_url = f"data:image/jpeg;base64,{encoded}"
       
    # build prompt and perform inference
    prompt    = prompt_template(image_url)
    response  = modelGemini(prompt)
    logger.info("Model response recieved.")

    # process output
    parsed    = list_validator(response)
    dataframe = convert_to_dataframe(parsed)

    logger.info(f"Image processed successfully. {dataframe['Parent Category'].nunique()} categories & {dataframe['Item Name'].nunique()} items extracted.")
    return dataframe
            
def multiimage(image_streams):

    dfs = []

    # process and store all image streams
    for i, image in enumerate(image_streams):
        dfs.append(vlm(image))

    # merge
    df = pd.concat(dfs, ignore_index=True)
    return df

def pipeline(image_stream, file_stream):
    
    logger.info("Files recieved. Processing started.")

    # extract menu
    dataframe = multiimage(image_stream)

    # merge non-existent items with scraped file
    file = pd.read_excel(file_stream, sheet_name=None)
    file['items'], missing_items = merge(dataframe, file['items'])
    file['items'] = additional_columns(file['items'])
    logger.info(f"Scraped and OCR files merged successfully. {missing_items['Item Name'].nunique()} additional items added.")

    # convert to aio format
    output = convert_to_aio(file)
    logger.info("File converted to AIO format.")

    # apply super menu
    #logger.info("Super Menu modifier/option filling added.")

    return output