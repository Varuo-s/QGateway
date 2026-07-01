from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.app.api.routes import router
from backend.app.config.settings import get_settings
from backend.app.logging.logger import get_logger

settings = get_settings()
logger = get_logger("main")

app = FastAPI(title="QGateway", version=settings.gateway.version)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

frontend_dist = settings.project_root / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=frontend_dist / "assets"), name="assets")


@app.get("/")
def index():
    index_file: Path = frontend_dist / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"service": "QGateway", "message": "Frontend has not been built yet."}


logger.info("QGateway backend initialized")

