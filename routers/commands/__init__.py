__all__ = ("router",)

from aiogram import Router
from .base_commands import router as base_router
from .notes_commands import router as notes_router


router = Router(name=__name__)

router.include_routers(
    base_router,
    notes_router,
)