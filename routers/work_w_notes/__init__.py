__all__ = ("router", )

from aiogram import Router
from .handle_command_notes import router as handle_notes_router

router = Router(name=__name__)

router.include_routers(
    handle_notes_router,
)