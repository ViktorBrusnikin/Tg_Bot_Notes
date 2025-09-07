from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.common_keyboards import abstract_kb_builder, exit_kb
from routers.work_w_notes.states import Notes
from tools.convert_path import convert_filename_to_path

router = Router(name=__name__)


@router.message(Command('open'))
async def handle_command_open(message: types.Message, state: FSMContext):
    await message.answer(
        text="📂 Введите название заметки, которую хотите открыть.",
        reply_markup=exit_kb(),
    )

    await state.set_state(Notes.open_note)


@router.message(Notes.open_note, F.text)
async def handle_open_note(message: types.Message, state: FSMContext):
    filename = message.text.strip()

    filepath = convert_filename_to_path(message.from_user.id, filename)

    if not filepath:
        await message.answer("⚠️ Файл с таким названием не найден.")
        return

    await message.answer(
        text=(
            f"✅ Файл <b>{filename}.md</b> успешно открыт!\n"
            "Теперь вы можете продолжать записывать или редактировать свои мысли."
        ),
        reply_markup=abstract_kb_builder(),
    )

    await state.update_data(filepath=filepath)
    await state.set_state(Notes.abstract)


@router.message(Notes.open_note)
async def handle_invalid_open_note(message: types.Message):
    await message.answer(
        text=(
            "❗ Пожалуйста, введите только название заметки.\n"
            "Чтобы выйти из режима открытия заметки — используйте кнопку «Главное меню»."
        ),
        reply_markup=exit_kb(),
    )