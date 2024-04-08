# from pydantic import BaseModel

# class User(BaseModel):
#     name: str
#     email: str
#     password: str

from pydantic import BaseModel, Field

class Address(BaseModel):
    city: str = Field(..., description="City of residence")    #ellipsis (...) is used to making the parameter mandatory  so city will be mandatory to be given as input
    country: str = Field(..., description="Country of residence")

class Student(BaseModel):
    name: str = Field(..., description="Student's name")
    age: int = Field(..., description="Student's age")
    address: Address = Field(..., description="Student's address")

# Define a Pydantic model for the response as FastAPI framework is trying to use a dictionary as a response model (in POST student), but it expects a Pydantic model instead. 
class ResponseModel(BaseModel):
    id: str

class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    address: dict | None = None