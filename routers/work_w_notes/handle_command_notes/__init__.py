__all__ = ("router", )

from aiogram import Router
from .open import router as open_router
from .create import router as create_router
from .all import router as all_router
from .change import router as change_router
from .merge import router as merge_router
from .handle_command_inside_notes import router as command_inside_router
from .handle_writer import router as writer_router
from .delete_note import router as delete_note_router
from .handle_garbage import router as garbage_router

router = Router(name=__name__)

router.include_routers(
    open_router,
    create_router,
    all_router,
    change_router,
    merge_router,
    command_inside_router,
    writer_router,
    delete_note_router,
    garbage_router,
)