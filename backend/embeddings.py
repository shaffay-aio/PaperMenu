import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from langchain.embeddings.openai import OpenAIEmbeddings

# Load environment variables (API key)
load_dotenv()

### 🔹 Load OpenAI Embeddings Model
def load_embeddings_model():
    API_KEY = os.getenv('OPENAI_API_KEY')
    return OpenAIEmbeddings(api_key=API_KEY) 

### 🔹 Generate Embeddings
def get_embeddings(items):
    items = [str(i) for i in items if pd.notna(i)]  # Convert to string & remove NaN
    if not items:  # Edge case: If empty list, return empty array
        return np.array([])
    
    model = load_embeddings_model()
    return np.array(model.embed_documents(items))  # Return as NumPy array

### 🔹 Find Similar Items using Cosine Similarity
def find_similar_items(df1, df2, threshold=0.99):
    """Check which items in df1 exist in df2 using cosine similarity on embeddings."""
    
    # Drop NaNs to avoid issues
    df1 = df1.dropna(subset=['Item Name'])
    df2 = df2.dropna(subset=['Item Name'])
    
    # Convert Item Names to lists
    item_names_1 = df1['Item Name'].tolist()
    item_names_2 = df2['Item Name'].tolist()
    
    # Generate embeddings
    emb_1 = get_embeddings(item_names_1)
    emb_2 = get_embeddings(item_names_2)

    # Edge case: If either embeddings array is empty, return df2 unchanged
    if emb_1.size == 0 or emb_2.size == 0:
        return df2
    
    # Compute cosine similarity
    similarity_matrix = cosine_similarity(emb_1, emb_2)

    # Find items that already exist in df2
    existing_items = set()
    for i, item in enumerate(item_names_1):
        if np.max(similarity_matrix[i]) >= threshold:
            existing_items.add(item)
            print(f"Existing Item : ", item, np.max(similarity_matrix[i]))
        else:
            print("\n\n\n Not exist : ", existing_items, similarity_matrix[i])

    print("Similarity matrix : ", similarity_matrix)
    # Find missing items (i.e., those not found in df2)
    missing_items = df1[~df1['Item Name'].isin(existing_items)]

    print("\n\n", missing_items)
    missing_items.to_csv("temp.csv")
    # If missing items exist, append them to df2
    if not missing_items.empty:
        df2 = pd.concat([df2, missing_items], ignore_index=True)
    else:
        print("DF is empty")
    return df2

### 🔹 Merge DataFrames using Similarity Check
def merge(df1, df2):
    """Merge df1 into df2 by checking for existing items using embeddings & cosine similarity."""
    
    # Ensure both inputs are DataFrames
    if not isinstance(df1, pd.DataFrame) or not isinstance(df2, pd.DataFrame):
        raise TypeError("Both inputs to merge() must be pandas DataFrames")

    # Run similarity-based merging
    updated_df = find_similar_items(df1, df2)
    
    return updated_df