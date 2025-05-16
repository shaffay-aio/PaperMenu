import io
import uvicorn
from PIL import Image
from io import BytesIO
from typing import List
from fastapi import HTTPException
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.main import pipeline, multiimage
from backend.processing import convert_pdf_to_jpgs, convert_png_to_jpgs

from backend.utils.logging import setup_logger
logger = setup_logger(__name__)

import warnings 
warnings.filterwarnings("ignore")

# FastAPI application
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)
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

# TODO: additional column Modifier should be such that i can be reflected back to middleware
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