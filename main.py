import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from utils import findIntent, recommFinalQuery, recommQuestion, RAG, getProducts
from dotenv import load_dotenv
load_dotenv() 
import os 

catalog_client = chromadb.PersistentClient(path="catalog")
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                model_name="text-embedding-3-large",
                api_key = os.environ["OPENAI_API_KEY"]
            )
catalog_collection = catalog_client.get_collection(name="catalogs", embedding_function=openai_ef)

docs_client = chromadb.PersistentClient(path="docs")
docs_collection = docs_client.get_collection(name="docs", embedding_function=openai_ef)

query = input()
intent = findIntent(query)
print(intent)
if intent == "Recommendation":
    result = getProducts(query,catalog_collection)
    print(result)
    ques = recommQuestion(query)
    print(ques)
    answers = input()
    final_query = recommFinalQuery(query,answers)
    result = getProducts(final_query,catalog_collection)
    print(result)
else:
    results = docs_collection.query(
    query_texts=["What is the brand Philosophy?"], # Chroma will embed this for you
    n_results=5 
    )
    answer = RAG(results,query)
    print(answer)

