import importlib
import logging
from typing import Iterable

from fastapi import APIRouter

from app.core.config import settings

logger = logging.getLogger(__name__)


def _module_names() -> Iterable[str]:
    raw = settings.MODULES
    if not raw:
        return []
    return [name.strip() for name in raw.split(",") if name.strip()]


def load_module_routers() -> list[tuple[str, APIRouter]]:
    routers: list[tuple[str, APIRouter]] = []
    for name in _module_names():
        module_path = f"app.modules.{name}.routes"
        try:
            module = importlib.import_module(module_path)
        except Exception as exc:
            logger.warning("Module '%s' failed to import (%s). Skipping.", name, exc)
            continue

        router = getattr(module, "router", None)
        if router is None:
            logger.warning("Module '%s' has no 'router'. Skipping.", name)
            continue
        if not isinstance(router, APIRouter):
            logger.warning("Module '%s' router is not APIRouter. Skipping.", name)
            continue

        routers.append((name, router))

    return routers
