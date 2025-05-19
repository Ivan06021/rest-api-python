import uvicorn
from fastapi import FastAPI
from routes import router


app = FastAPI()

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
