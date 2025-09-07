__all__ = ("router",)

from aiogram import Router
from .commands import router as commands_router
from .work_w_notes import router as handle_w_notes_router

router = Router(name=__name__)

router.include_routers(
    commands_router,
    handle_w_notes_router,
)