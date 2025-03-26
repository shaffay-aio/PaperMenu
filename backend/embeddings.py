import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from fastapi import HTTPException
from sklearn.metrics.pairwise import cosine_similarity
from langchain.embeddings.openai import OpenAIEmbeddings

load_dotenv()

def load_embeddings_model():

    API_KEY = os.getenv('OPENAI_API_KEY')
    return OpenAIEmbeddings(api_key=API_KEY) 

def get_embeddings(items):

    items = [str(i) for i in items if pd.notna(i)] 
    if not items:  # Edge case: If empty list, return empty array
        return np.array([])
    
    model = load_embeddings_model()
    return np.array(model.embed_documents(items))

def find_similar_items(df1, df2, threshold=0.99):
    
    # Drop nans and get list
    df1 = df1.dropna(subset=['Item Name'])
    df2 = df2.dropna(subset=['Item Name'])
    
    item_names_1 = df1['Item Name'].tolist()
    item_names_2 = df2['Item Name'].tolist()
    
    # Generate embeddings & Compute similarity
    emb_1 = get_embeddings(item_names_1)
    emb_2 = get_embeddings(item_names_2)

    # Edge case: If either embeddings array is empty, return df2 unchanged
    if emb_1.size == 0 or emb_2.size == 0:
        return df2
    
    similarity_matrix = cosine_similarity(emb_1, emb_2)

    # Find items that already exist in df2, separate missing items
    existing_items = set()
    for i, item in enumerate(item_names_1):
        if np.max(similarity_matrix[i]) >= threshold:
            existing_items.add(item)

    missing_items = df1[~df1['Item Name'].isin(existing_items)]

    # If missing items exist, append them to df2
    if not missing_items.empty:
        df2 = pd.concat([df2, missing_items], ignore_index=True)

    return df2, missing_items

def merge(df1, df2):

    try:
        df, missing_items = find_similar_items(df1, df2)
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Dataframe merging error. {e}")

    return df, missing_items