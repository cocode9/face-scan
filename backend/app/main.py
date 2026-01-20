from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth_routes
from .database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth API")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)