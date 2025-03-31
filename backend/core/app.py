import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import test, api, auth, register, users, user_usage, admin_usage, admin_stats, lumisenseai
import models  # noqa: F401
from core.usage_middleware import UsageMiddleware

load_dotenv()
BASE_URL = os.getenv("BASE_PREFIX", "")

print(f"🔴🟥Debugging base url: {BASE_URL}")


def create_app():
    app = FastAPI()

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "*",
            "http://localhost:5173",
            "https://bcit-anthony-sh-s.com",
            "https://dolphin-app-kdrrc.ondigitalocean.app",
            "https://www.bcit-anthony-sh-s.com",
            "https://www.dolphin-app-kdrrc.ondigitalocean.app"
            ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register Each Service

    app.include_router(test.router, prefix=f"{BASE_URL}")
    app.include_router(api.router, prefix=f"{BASE_URL}/api", tags=["api"])
    app.include_router(auth.router, prefix=f"{BASE_URL}/auth", tags=["auth"])
    app.include_router(
        users.router, prefix=f"{BASE_URL}/users", tags=["users"]
        )
    app.include_router(
        register.router,
        prefix=f"{BASE_URL}",
        tags=["register"]
        )
    app.include_router(user_usage.router, prefix=f"{BASE_URL}/users", tags=["users"])
    app.include_router(admin_usage.router, prefix=f"{BASE_URL}/admin", tags=["admin"])
    app.include_router(admin_stats.router, prefix=f"{BASE_URL}/admin/stats", tags=["admin_stats"])
    app.include_router(lumisenseai.router, prefix=f"{BASE_URL}/lumisenseai", tags=["lumisenseai"])


    # Initialize Database
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"⚠️ Database initialization failed: {e}")

    app.add_middleware(UsageMiddleware)

    return app
