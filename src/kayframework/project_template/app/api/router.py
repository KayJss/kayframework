from fastapi import APIRouter
from app.auth.routes import router as auth_router
from app.modules.loader import load_module_routers

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])

for name, router in load_module_routers():
    api_router.include_router(router, prefix=f"/modules/{name}", tags=[f"module:{name}"])
