from importlib import import_module
import logging

from fastapi import FastAPI

from app.core.config import settings

logger = logging.getLogger(__name__)


def register_plugins(app: FastAPI) -> None:
    plugin_names = [item.strip() for item in settings.PLUGINS.split(",") if item.strip()]
    for plugin_name in plugin_names:
        module = import_module(f"app.plugins.{plugin_name}")
        register = getattr(module, "register", None)
        if not callable(register):
            raise RuntimeError(f"Plugin '{plugin_name}' must expose register(app, settings)")
        register(app, settings)
        logger.info("Loaded plugin: %s", plugin_name)
