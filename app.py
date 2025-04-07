import io
import uvicorn
import pandas as pd
from io import BytesIO
from typing import List
from fastapi import HTTPException
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.main import pipeline, multiimage

from backend.utils.logging import setup_logger
logger = setup_logger(__name__)

import warnings 
warnings.filterwarnings("ignore")

# FastAPI application
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

async def read_images(images: List[UploadFile]):

    # TODO: image should be jpg error
    image_streams = []
    
    # Read all images into byte streams first
    for image in images:

        try:
            image_bytes = await image.read()
            image_stream = BytesIO(image_bytes)
            image_streams.append(image_stream)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error while reading image {image.filename}. {e}")

    return image_streams

@app.post("/ocr")
async def ocr_only(images: List[UploadFile] = File(...)):

    # Read and process the image
    image_streams = await read_images(images)

    try:
        response = multiimage(image_streams)
        
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error. {e}")

    # convert excel file to byte stream object
    output = io.BytesIO() 
    response.to_csv(output, index=False)    
    output.seek(0)

    filename = "file.csv"
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={filename}"})

@app.post("/ocr-menu-pipeline")
async def OCR(images: List[UploadFile] = File(...), file: UploadFile = File(...)):

    # Read and process the image
    image_streams = await read_images(images)
    
    # Read the excel file
    file_data = await file.read()
    file_stream = BytesIO(file_data)

    try:
        output = pipeline(image_streams, file_stream)

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error. {e}")

    filename = "file.xlsx"
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": f"attachment; filename={filename}"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8042)