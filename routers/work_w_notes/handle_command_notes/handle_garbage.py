from aiogram import Router, types

from keyboards.common_keyboards import exit_kb

router = Router(name=__name__)


@router.message()
async def handle_garbage(message: types.Message):
    await message.answer(
        text="Я вас не понимаю...",
        reply_markup=exit_kb(),
    )