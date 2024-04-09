# from pymongo import MongoClient
# # conn=MongoClient("mongodb://localhost:27017/test")
# conn=MongoClient()

from pymongo import MongoClient

MONGODB_URI = "mongodb://localhost:27017/"  

client = MongoClient(MONGODB_URI)
db = client["StudentsDatabase"]  
students_collection = db["students"]  
