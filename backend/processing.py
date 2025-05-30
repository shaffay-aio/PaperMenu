import ast
import fitz  # PyMuPDF
import requests
import io, base64
import pandas as pd
from PIL import Image
from io import BytesIO
from typing import List
from fastapi import HTTPException, UploadFile
from backend.utils.logging import setup_logger

logger = setup_logger(__name__)

def convert_pdf_to_jpgs(file_bytes):

    images = []
    pdf = fitz.open(stream=file_bytes, filetype="pdf")

    for page_num in range(len(pdf)):
    
        page = pdf.load_page(page_num)
        pix = page.get_pixmap(dpi=200) 
    
        img_stream = BytesIO(pix.tobytes("jpeg"))    
        images.append(img_stream)

        #pix.save(f"{page_num}.jpg")
    return images

def convert_png_to_jpgs(png_bytes):
  
    pil_img = Image.open(BytesIO(png_bytes)).convert("RGB")
    jpg_stream = BytesIO()

    pil_img.save(jpg_stream, format="JPEG")
    jpg_stream.seek(0)
    
    return jpg_stream

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
            #img = img.resize((1000, 1000), Image.Resampling.LANCZOS)
            
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

        # preprocess columns
        df.columns = ["Parent Category", "Item Name", "Item Price", "Item Description"]
        df[['Parent Category', 'Item Name']] = df[['Parent Category', 'Item Name']].apply(lambda col: col.apply(lambda val: val.title() if pd.notna(val) else val))
        
        #df['Item Price'] = df['Item Price'].apply(
        #    lambda x: float(re.sub(r'[^0-9.]', '', str(x))) if pd.notna(x) and str(x).strip() != '' else None
        #)
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
    
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "pdf"}
async def read_images(images: List[UploadFile]):
    image_streams = []

    for image in images:
        filename = image.filename.lower()

        ext = filename.split('.')[-1]
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"Unsupported file format for file {filename}. Allowed formats: jpg, jpeg, png, pdf.")

        try:
            file_bytes = await image.read()

            if ext in {"jpg", "jpeg"}:
                image_streams.append(BytesIO(file_bytes))

            elif ext == "png":
                jpg_stream = convert_png_to_jpgs(file_bytes)
                image_streams.append(jpg_stream)
                
            elif ext == "pdf":
                image_streams.extend(convert_pdf_to_jpgs(file_bytes))


        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error while processing {filename}. {e}")

    return image_streams

def dump_to_middleware(df):

    format = pd.read_excel('./resources/Sample Middleware File Format.xlsx', sheet_name=None)
    
    # extracted values
    format['items']['Parent Category'] = df['Parent Category']
    format['items']['Item Name'] = df['Item Name']
    format['items']['Item Price'] = df['Item Price']
    format['items']['Item Description'] = df['Item Description']

    # default values
    format['items']['Menu Name'] = ['Main Menu'] * len(format['items'])
    format['items']['Stock Status'] = ['inStock'] * len(format['items'])

    return format