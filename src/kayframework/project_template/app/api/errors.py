from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException


templates = Jinja2Templates(directory="app/templates")


def _wants_html(request: Request) -> bool:
    accept = request.headers.get("accept", "")
    return "text/html" in accept.lower()


def _error_payload(exc: Exception) -> dict:
    if isinstance(exc, StarletteHTTPException):
        return {"status_code": exc.status_code, "detail": exc.detail}
    if isinstance(exc, RequestValidationError):
        return {"status_code": status.HTTP_422_UNPROCESSABLE_ENTITY, "detail": exc.errors()}
    return {"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR, "detail": "Internal Server Error"}


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        payload = _error_payload(exc)
        if _wants_html(request):
            return templates.TemplateResponse(
                "error.html",
                {"request": request, **payload},
                status_code=payload["status_code"],
            )
        return JSONResponse(status_code=payload["status_code"], content={"detail": payload["detail"]})

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        payload = _error_payload(exc)
        if _wants_html(request):
            return templates.TemplateResponse(
                "error.html",
                {"request": request, **payload},
                status_code=payload["status_code"],
            )
        return JSONResponse(status_code=payload["status_code"], content={"detail": payload["detail"]})

    @app.exception_handler(Exception)
    async def internal_exception_handler(request: Request, exc: Exception):
        payload = _error_payload(exc)
        if _wants_html(request):
            return templates.TemplateResponse(
                "error.html",
                {"request": request, **payload},
                status_code=payload["status_code"],
            )
        return JSONResponse(status_code=payload["status_code"], content={"detail": payload["detail"]})
