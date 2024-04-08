from fastapi import FastAPI  # Assuming FastAPI is installed at the top level
from routes import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)  # Change port if needed