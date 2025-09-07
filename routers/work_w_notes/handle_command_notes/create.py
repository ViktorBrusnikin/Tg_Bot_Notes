from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.common_keyboards import exit_kb, abstract_kb_builder
from routers.work_w_notes.states import Notes
from tools.create_dir import sanitize_name, unique_md_path, ensure_user_dir

router = Router(name=__name__)


@router.message(Command('create'))
async def handle_command_create(message: types.Message, state: FSMContext):
    await state.set_state(Notes.create_note)
    await message.answer(
        text=(
            "💡 Давайте создадим новую заметку!\n\n"
            "Введите уникальное название — оно поможет легко найти заметку позже."
        ),
        reply_markup=exit_kb(),
    )


@router.message(Notes.create_note, F.text)
async def handle_create_note(message: types.Message, state: FSMContext):
    # получаем сырое название от пользователя
    raw_filename = message.text.strip()

    # безопасность — получаем id пользователя (fallback на chat id если from_user нет)
    user_id = message.from_user.id if message.from_user else message.chat.id

    # санитизация имени
    safe_name = sanitize_name(raw_filename)
    if not safe_name:
        await message.answer("Некорректное название файла, попробуйте ещё раз")
        return

    # создаём директорию пользователя и получаем уникальный путь
    user_dir = ensure_user_dir(user_id)
    filepath = unique_md_path(user_dir, safe_name)

    # создаём файл и записываем заголовок
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {safe_name}\n\n")

    # сохраняем путь в state (строка)
    await state.update_data(filepath=str(filepath), filename=safe_name, user_dir=str(user_dir))

    await state.set_state(Notes.abstract)

    # Если имя изменилось (добавлен суффикс), скажем пользователю об этом
    created_name = filepath.name
    await message.answer(
        text=(
            f"🎉 Файл {created_name} успешно создан!\n"
            "Теперь вы можете начать записывать свои мысли и идеи."
        ),
        reply_markup=abstract_kb_builder(),
    )


@router.message(Notes.create_note)
async def handle_error_create_note(message: types.Message):
    await message.answer(
        text=(
            "⚠️ Похоже, что введённые данные некорректны.\n"
            "Попробуйте ещё раз, выбрав уникальное название для заметки."
        ),
        reply_markup=exit_kb(),
    )
