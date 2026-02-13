import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.router import api_router
from app.api.errors import register_exception_handlers
from app.core.config import settings

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI(title="KAYFRAMEWORK API")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(api_router)
register_exception_handlers(app)
@app.get("/")
def home(request: Request):
    accept = request.headers.get("accept", "")
    if "text/html" in accept.lower():
        return templates.TemplateResponse("home.html", {"request": request})
    return {"status": "Sistem Ayakta"}
