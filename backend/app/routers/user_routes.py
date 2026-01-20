from fastapi import FastAPI
from .routers import auth_routes
from .database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth API")
app.include_router(auth_routes.router)
