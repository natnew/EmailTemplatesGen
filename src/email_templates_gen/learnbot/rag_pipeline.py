from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

def load_index(openai_api_key=None):
    loader = DirectoryLoader("docs", glob="**/*.md")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    if openai_api_key is None:
        openai_api_key = os.getenv("OPENAI_API_KEY")

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    db = FAISS.from_documents(chunks, embeddings)
    return db
