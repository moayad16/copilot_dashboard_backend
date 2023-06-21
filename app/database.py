from pymongo import MongoClient
from app.settings import mongodb_uri

client = MongoClient(mongodb_uri)

db = client.copilot_dashboard

users_collection = db.users
