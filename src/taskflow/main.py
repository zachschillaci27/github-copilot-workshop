"""TaskFlow API - Main application entry point."""

from fastapi import FastAPI

from taskflow.routers import tasks, users

app = FastAPI(
    title="TaskFlow API",
    description="A task management API for the GitHub Copilot workshop",
    version="0.1.0",
)

app.include_router(tasks.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")


@app.get("/")
def root() -> dict:
    """Root endpoint with API info."""
    return {
        "name": "TaskFlow API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}
