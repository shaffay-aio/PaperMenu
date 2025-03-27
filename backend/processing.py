import ast
import requests
import io, base64
import pandas as pd
from PIL import Image
from fastapi import HTTPException
from backend.utils.logging import setup_logger

logger = setup_logger(__name__)

def create_bytes_object(file):

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for key in file.keys():
            file[key].to_excel(writer, sheet_name=key, index=False)            
    output.seek(0)

    return output

def encode_image(image_path):
    
    try:
        # Open the image file
        with Image.open(image_path) as img:

            # Resize the image using high-quality downsampling
            img = img.resize((1000, 1000), Image.Resampling.LANCZOS)
            
            # Save the resized image to a byte buffer
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            
            # Encode the image to base64
            return base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Image conversion error. {e}")

def list_validator(response):

    try:
        output = ast.literal_eval(response)
        return output 
    except Exception as e:
        with open("./output/response.txt", "a") as f:
            f.write(response)
        raise HTTPException(status_code=403, detail=f"List conversion error. {e}")
    
def convert_to_dataframe(output):
   
    try:
        df = pd.DataFrame(output)
        df.columns = ["Parent Category", "Item Name", "Item Price", "Item Description"]
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Dataframe creation error. {e}")

    return df

def additional_columns(dataframe):

    dataframe['Menu Name'] = ['Main Menu'] * len(dataframe)
    dataframe['Stock Status'] = ['inStock'] * len(dataframe)
    return dataframe

def convert_to_aio(file):

    # convert excel file to bytes object
    byte = create_bytes_object(file)

    # prepare payload
    url = "http://44.231.228.32:8040/onlinetoaioformatter"
    files = {"file": ("data.xlsx", byte, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}

    # hit endpoint get response
    response = requests.post(url, files=files)

    # read file
    if response.status_code == 200:
        logger.info("AIO format api completed.")        
        df = pd.read_excel(response.content, sheet_name=None)
        output = create_bytes_object(df)
        return output
    else:
        logger.info("AIO format api failed.")
        raise HTTPException(status_code=response.status_code, detail=response.text)