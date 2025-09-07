import os
from aiogram import Router, types
from aiogram.filters import Command

from keyboards.common_keyboards import exit_kb
from tools.create_dir import get_user_dir

router = Router(name=__name__)


@router.message(Command('all'))
async def handle_command_all(message: types.Message):
    user_id = message.from_user.id
    user_dir = get_user_dir(user_id)

    # Если у пользователя ещё нет папки
    if not user_dir.exists():
        await message.answer(
            text=(
                "📭 У вас пока нет ни одной заметки.\n"
                "Создайте новую заметку командой /create и начните конспектировать свои мысли."
            )
        )
        return

    files = os.listdir(user_dir)
    notes = [f[:-3] for f in files if f.endswith(".md")]

    if not notes:
        await message.answer(
            text=(
                "📭 У вас пока нет ни одной заметки.\n"
                "Создайте новую заметку командой /create и начните конспектировать свои мысли."
            )
        )
    else:
        notes_list = "\n".join(notes)
        await message.answer(
            text=(
                "🗒 Вот список ваших заметок:\n\n"
                f"{notes_list}\n\n"
                "Вы можете открыть любую из них командой /open."
            ),
            reply_markup=exit_kb(),
        )