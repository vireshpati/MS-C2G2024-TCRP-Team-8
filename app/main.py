from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import users, staff

app = FastAPI(title="Community Chat App")

# Include routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(staff.router, prefix="/staff", tags=["staff"])

# Serve static files (for frontend)
app.mount("/", StaticFiles(directory="app/frontend", html=True), name="frontend")

