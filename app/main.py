from fastapi import FastAPI
from .crud import post_C, user_C

app = FastAPI(title="Secure Blog API")

app.include_router(user_C.router, prefix="", tags=["Authentication"])
app.include_router(post_C.router, prefix="", tags=["Posts"])

@app.get("/")
def home():
    return {"message": "Welcome to the Blog API!"}