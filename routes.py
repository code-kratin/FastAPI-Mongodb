# from fastapi import APIRouter

# from models.user import User
# from config.db import conn

# user=APIRouter()

# @user.get('/')
# async def find_all_users():
#     return conn.local.user.find()
# Create a new student
from fastapi import FastAPI, Body, Path, Query, HTTPException, status
from models import Student, ResponseModel, StudentUpdate
from config import students_collection
from bson.objectid import ObjectId   #In pymongo 2.2 the call to import objectid is changed

app = FastAPI()



@app.post("/students", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def create_student(student: Student):
    student_dict = student.dict()
    result = students_collection.insert_one(student_dict)
    new_student = students_collection.find_one({"_id": result.inserted_id})
    return {"id": str(result.inserted_id)}

# Get all students with optional filters
@app.get("/students", response_model=list[Student])
async def get_all_students(country: str | None = Query(default=None, description="To apply filter of country. If not given or empty, this filter should be applied."),
                           age: int | None = Query(default=None, gt=0, description="Only records which have age greater than equal to the provided age should be present in the result. If not given or empty, this filter should be applied.")):
   
    # filter logic based on country and age
    filters = {}
    if country:
        filters["address.country"] = country
    if age:
        filters["age"] = {"$gte": age}  # Greater than or equal to age

    students = students_collection.find(filters)
    return [Student(**student) for student in students] 

# Get a student by ID
@app.get("/students/{student_id}", response_model=Student)
async def get_student_by_id(student_id: str):
    student = students_collection.find_one({"_id": ObjectId(student_id)})

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    # Ensure required fields are present (although likely already enforced by model validation)
    if not all(field in student for field in ("name", "age", "address")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student data is missing required fields",
        )

    return Student(**student)   #or create a schema and return SchemaName(student) as student is a object cant be directly returned, similar to the Student model itself but it can contian Id as a field 

# Update a student by ID (partial update with PATCH)

@app.patch("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_student(student_id: str = Path(..., description="The ID of the student to be updated."),
                         updated_data: Student = Body(..., description="Student data to be updated")):
    # Filter for student by ID
    student = students_collection.find_one({"_id": ObjectId(student_id)})
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    # Prepare update data (only update provided fields)
    update_dict = updated_data.dict(exclude_unset=True)

    # Update the student document
    result = students_collection.update_one({"_id": ObjectId(student_id)}, {"$set": update_dict})

    # Handle update result (optional: you can return the updated document here)
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    return None  # No content response (204)


# Delete a student by ID
@app.delete("/students/{student_id}", status_code=status.HTTP_200_OK)
async def delete_student(student_id: str = Path(..., description="The ID of the student to delete.")):
    try:
        # Delete the student using ObjectId for accurate ID matching
        result = students_collection.delete_one({"_id": ObjectId(student_id)})

        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

        return {"message": "Student deleted successfully"}  # Return a simple success message

    except Exception as e:  # Catch potential errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
