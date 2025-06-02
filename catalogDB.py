import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import pandas as pd

chroma_client = chromadb.PersistentClient(path="catalog")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                #api_key="YOUR_API_KEY",
                model_name="text-embedding-3-large"
            )
collection = chroma_client.get_collection(name="catalogs", embedding_function=openai_ef)
file_path = "/content/skincare catalog.xlsx"
xls = pd.ExcelFile(file_path)
sheet_names = xls.sheet_names
df = xls.parse(sheet_names[0])

# Prepare the data for Chroma collection
documents = []
metadatas = []
ids = []

for _, row in df.iterrows():
    # Create the document by concatenating relevant columns
    document = f"{row['name']}. Category: {row['category']}. Description: {row['description']}. " \
               f"Top Ingredients: {row['top_ingredients']}. Tags: {row['tags']}."
    
    # Create metadata
    metadata = {
        "price": row["price (USD)"],
        "margin": row["margin (%)"],
        "Name": row['name']
    }
    
    # Append to lists
    documents.append(document)
    metadatas.append(metadata)
    ids.append(row["product_id"])

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

