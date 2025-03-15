from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from typing import Annotated
from utils.auth import authenticate_user


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/api/test")
def test_api():
    return {"message": "API is working!"}


try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")
except Exception as e:
    print(f"⚠️ Database initialization failed: {e}")


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(SessionLocal)):
    user = authenticate_user(db, form_data.username)


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    print(f"🚀 FastAPI server running at: http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)
