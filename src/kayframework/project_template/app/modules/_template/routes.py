from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def module_root():
    return {"module": "_template", "status": "ok"}
