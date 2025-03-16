import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import ai, test, api, auth, register, user_dashboard
import models  # noqa: F401

load_dotenv()
BASE_URL = os.getenv("BASE_PREFIX", "")

print(f"🔴🟥Debugging base url: {BASE_URL}")


def create_app():
    app = FastAPI()

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register Each Service

    app.include_router(test.router)
    app.include_router(ai.router, prefix=f"{BASE_URL}/ai", tags=["ai"])
    app.include_router(api.router, prefix=f"{BASE_URL}/api", tags=["api"])
    app.include_router(auth.router, prefix=f"{BASE_URL}/auth", tags=["auth"])
    app.include_router(
        auth.router, prefix="/{BASE_URL}//users", tags=["users"]
        )
    app.include_router(register.router, tags=["register"])
    app.include_router(
        user_dashboard.router,
        prefix=f"/{BASE_URL}/user-dashboard",
        tags=["User Dashboard"]
        )

    # Initialize Database
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"⚠️ Database initialization failed: {e}")
    return app
