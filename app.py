
# fastapi endpoint
# - accepts multiple images (jpg), and an excel file
# calls main process
# returns final csv

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import warnings 
warnings.filterwarnings("ignore")

# FastAPI application
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)

@app.post("/supermenu")
def ocr():
    pass 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8041)