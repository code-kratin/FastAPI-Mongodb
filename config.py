# from pymongo import MongoClient
# # conn=MongoClient("mongodb://localhost:27017/test")
# conn=MongoClient()

from pymongo import MongoClient

MONGODB_URI = "mongodb://localhost:27017/"  # Update with your actual connection string

client = MongoClient(MONGODB_URI)
db = client["StudentsDatabase"]  # Replace with your database name
students_collection = db["students"]  # Replace with your collection name