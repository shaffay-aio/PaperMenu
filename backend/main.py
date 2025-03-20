from backend.model import prompt_template, model
from backend.processing import encode_image, json_validator, convert_to_dataframe

import os
import openai
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def vlm(image_stream):

    # process image
    encoded   = encode_image(image_stream)
    image_url = f"data:image/jpeg;base64, {encoded}"
    
    # build prompt and perform inference
    prompt    = prompt_template(image_url)
    response  = model(prompt)

    # process output
    parsed    = json_validator(response)
    dataframe = convert_to_dataframe(parsed)

    return dataframe

def generate_embeddings(text_list):

    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Embedding.create(
        input=text_list,
        model="text-embedding-ada-002"
    )
    embeddings = [embedding['embedding'] for embedding in response['data']]
    return np.array(embeddings)

def get_unmatched(df_embeddings, similarities, threshold=0.85):

    unmatched_items = []

    for i, row in df_embeddings.iterrows():
        max_similarity = np.max(similarities[i])

        if max_similarity < threshold:
            unmatched_items.append(row)

    return unmatched_items
            
def merge(dataframe, file_stream):

    # get embeddings
    df_embeddings = generate_embeddings(dataframe['Item Name'].tolist())
    fs_embeddings = generate_embeddings(file_stream['Item Name'].tolist())

    # extract unfamiliar items
    similarities  = cosine_similarity(df_embeddings, fs_embeddings)
    unmatched     = get_unmatched(df_embeddings, similarities)

    # add to online file 
    unmatched_df  = pd.concat([file_stream, unmatched], ignore_index=True)
    return unmatched_df

def pipeline(image_stream, file_stream):
    
    dataframe = vlm(image_stream)
    merged    = merge(dataframe, file_stream)

    pass