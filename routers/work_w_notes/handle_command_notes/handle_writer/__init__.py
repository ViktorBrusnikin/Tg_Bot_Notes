__all__ = ("router", )

from aiogram import Router

from .handle_state_abstract import router as state_abstract_router

router = Router(name=__name__)

router.include_routers(
    state_abstract_router,
)