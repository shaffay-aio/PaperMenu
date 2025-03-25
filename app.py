import io
import uvicorn
import pandas as pd
from io import BytesIO
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.main import pipeline, vlm

from backend.utils.logging import setup_logger
logger = setup_logger(__name__)

import warnings 
warnings.filterwarnings("ignore")

# FastAPI application
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

@app.post("/ocr")
async def ocr_only(image: UploadFile = File(...)):

    # Read and process the image
    image_bytes = await image.read()
    image_stream = BytesIO(image_bytes)

    response = vlm(image_stream)

    # convert excel file to byte stream object
    output = io.BytesIO() 
    response.to_csv(output, index=False)    
    output.seek(0)

    filename = "file.csv"
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={filename}"})

@app.post("/ocr-menu-pipeline")
async def OCR(image: UploadFile = File(...), file: UploadFile = File(...)):

    # Read and process the image
    image_bytes = await image.read()
    image_stream = BytesIO(image_bytes)
    
    # Read the excel file
    file_data = await file.read()
    file_stream = BytesIO(file_data)

    output = pipeline(image_stream, file_stream)
    filename = "file.xlsx"
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": f"attachment; filename={filename}"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8042)