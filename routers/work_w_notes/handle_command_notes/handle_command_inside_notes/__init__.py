__all__ = ("router", )

from aiogram import Router
from .view import router as view_router
from .note import router as note_router
from .edit import router as edit_router
from .delete_thought import router as delete_router
from .handle_back_to_abstract import router as back_to_abstract_router


router = Router(name=__name__)

router.include_routers(
    back_to_abstract_router,
    view_router,
    note_router,
    edit_router,
    delete_router,
)