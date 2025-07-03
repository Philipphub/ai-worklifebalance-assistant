from fastapi import FastAPI
from app.api.v1 import router as api_v1_router

app = FastAPI(
    title="AI-Powered Work-Life Balance Assistant",
    description="An API for analyzing schedules to improve work-life balance.",
    version="1.0.0",
)

# Include the API router
app.include_router(api_v1_router.router, prefix="/api/v1")


@app.get("/", tags=["Health Check"])
def read_root():
    """A simple health check endpoint."""
    return {"status": "ok"}
