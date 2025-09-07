from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.common_keyboards import exit_kb, menu_kb_builder
from routers.work_w_notes.states import Notes
from tools.create_dir import get_user_dir, sanitize_name

router = Router(name=__name__)


@router.message(Command('delete_note'))
async def handle_command_delete_note(message: types.Message, state: FSMContext):
    await message.answer(
        text=(
            "🗑 Введите название заметки, которую хотите удалить.\n"
            "Будьте внимательны — действие необратимо!"
        ),
        reply_markup=exit_kb(),
    )
    await state.set_state(Notes.delete_note)


@router.message(Notes.delete_note, F.text)
async def handle_state_delete_note(message: types.Message, state: FSMContext):
    user_dir = get_user_dir(message.from_user.id)  # личная директория
    note_name = sanitize_name(message.text.strip())
    filepath = user_dir / f"{note_name}.md"

    if not filepath.exists():
        await message.answer(
            text=(
                "⚠️ Заметка с таким названием не найдена.\n"
                "Проверьте правильность написания или используйте /all, чтобы увидеть список всех заметок."
            ),
            reply_markup=exit_kb(),
        )
        return

    try:
        filepath.unlink()  # удаляем файл
        await message.answer(
            text=(
                f"✅ Заметка «{note_name}» успешно удалена!\n"
                "Вы можете продолжить работу с другими заметками через главное меню."
            ),
            reply_markup=menu_kb_builder(),
        )
    except Exception:
        await message.answer(
            text=(
                f"❌ Не удалось удалить заметку «{note_name}».\n"
                "Попробуйте ещё раз или проверьте права доступа к файлу."
            ),
            reply_markup=exit_kb(),
        )

    await state.clear()


@router.message(Notes.delete_note)
async def handle_state_delete_note(message: types.Message):
    await message.answer(
        text=(
            "⚠️ Пожалуйста, введите только название заметки для удаления.\n"
            "Чтобы выйти из режима удаления, используйте кнопку «Выйти»."
        ),
        reply_markup=exit_kb(),
    )