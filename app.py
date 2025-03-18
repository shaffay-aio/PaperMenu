
# fastapi endpoint
# - accepts multiple images (jpg), and an excel file
# calls main process
# returns final csv

import uvicorn
from io import BytesIO
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.main import vlm
    
import warnings 
warnings.filterwarnings("ignore")

# FastAPI application
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

# TODO: make it multi jpg uploader
@app.post("/supermenu")
async def OCR(image: UploadFile = File(...), file: UploadFile = File(...)):

    # Read and process the image
    image_bytes = await image.read()
    image_stream = BytesIO(image_bytes)
    
    # Read the excel file
    file_data = await file.read()
    file_stream = BytesIO(file_data)

    output = vlm(image_stream, file_stream)
    filename = "file.xlsx"
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": f"attachment; filename={filename}"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8042)