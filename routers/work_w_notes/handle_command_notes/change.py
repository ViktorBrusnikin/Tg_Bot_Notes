from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.common_keyboards import exit_kb, abstract_kb_builder
from routers.work_w_notes.states import Notes
from tools.convert_path import convert_filename_to_path

router = Router(name=__name__)

@router.message(Command('change'))
async def handle_command_change(message: types.Message, state: FSMContext):
    await message.answer(
        text=(
            "✏️ Введите название заметки, в которую хотите продолжить запись.\n"
        ),
        reply_markup=exit_kb(),
    )
    await state.set_state(Notes.choose_note)


@router.message(Notes.choose_note, F.text)
async def handle_choose_state(message: types.Message, state: FSMContext):
    filename = message.text.strip()

    filepath = convert_filename_to_path(message.from_user.id, filename)

    if not filepath:
        await message.answer(
            text=(
                "⚠️ Файл с таким названием не найден.\n"
            )
        )
        return

    await state.update_data(filepath=filepath)
    await state.set_state(Notes.abstract)

    await message.answer(
        text=(
            f"✅ Текущая заметка успешно изменена на <b>{filename}.md</b>!\n"
            "Теперь вы можете продолжать конспектировать свои мысли в этом файле."
        ),
        reply_markup=abstract_kb_builder(),
    )


@router.message(Notes.choose_note)
async def handle_invalid_choose_state(message: types.Message):
    await message.answer(
        text=(
            "⚠️ Пожалуйста, введите только название заметки.\n"
            "Чтобы выйти из режима выбора файла, используйте кнопку «Главное меню»."
        ),
        reply_markup=exit_kb(),
    )