from fastapi import FastAPI
from app.routes import users, sketches

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health-check")
async def root():
    return {"message": "OK"}

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(sketches.router, prefix="/sketches", tags=["sketches"])
