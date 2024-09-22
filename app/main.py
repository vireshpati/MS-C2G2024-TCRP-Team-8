from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import auth, users, fcm

app = FastAPI(title="Community Chat App")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(fcm.router, prefix="/fcm")

# Serve static files (for frontend)
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
