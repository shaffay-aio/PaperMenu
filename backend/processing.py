import ast
import io, base64
import pandas as pd
from PIL import Image
from fastapi import HTTPException

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
        raise HTTPException(status_code=403, detail=f"List conversion error. {e}")
    
def convert_to_dataframe(output):
   
    try:
        df = pd.DataFrame(output)
        df.columns = ["Category Name", "Item Name", "Item Price", "Item Description"]
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Dataframe creation error. {e}")

    return df