from pymongo import MongoClient 
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# read mongoDB url

MONGO_URI = os.getenv("MONGO_URL")

# create mongo connection 

client = MongoClient(MONGO_URI)


db = client["ai-doc-qa"]
documents_col = db["document"]

