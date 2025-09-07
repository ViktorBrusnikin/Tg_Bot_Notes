from pathlib import Path
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.common_keyboards import exit_kb
from routers.work_w_notes.states import MergeNotes
from tools.create_dir import get_user_dir, sanitize_name, ensure_user_dir

router = Router(name=__name__)


@router.message(Command('merge'))
async def handle_command_merge(message: types.Message, state: FSMContext):
    await message.answer(
        text=(
            "🔗 Давайте объединим две заметки!\n"
            "Введите название первой заметки, которую хотите объединить."
        ),
        reply_markup=exit_kb(),
    )
    await state.set_state(MergeNotes.first_file)


@router.message(MergeNotes.first_file, F.text)
async def handle_merge_firstfile(message: types.Message, state: FSMContext):
    user_dir = get_user_dir(message.from_user.id)  # путь до папки пользователя
    filename = sanitize_name(message.text.strip())
    filepath = user_dir / f"{filename}.md"

    if not filepath.exists():
        await message.answer(
            text=(
                "⚠️ Файл с таким названием не найден.\n"
                "Проверьте правильность написания и попробуйте ещё раз."
            )
        )
        return

    await state.update_data(first_filepath=filepath)
    await state.set_state(MergeNotes.second_file)

    await message.answer(
        text=(
            "Введите название второй заметки, которую хотите объединить с первой.\n"
            "Нельзя выбирать ту же заметку, что и первая."
        ),
        reply_markup=exit_kb(),
    )


@router.message(MergeNotes.first_file)
async def handle_invalid_merge_firstfile(message: types.Message):
    await message.answer(
        text=(
            "⚠️ Некорректные данные.\n"
            "Попробуйте ввести корректное название для новой заметки."
        ),
        reply_markup=exit_kb()
    )


@router.message(MergeNotes.second_file, F.text)
async def handle_merge_secondfile(message: types.Message, state: FSMContext):
    user_dir = get_user_dir(message.from_user.id)
    filename = sanitize_name(message.text.strip())
    filepath = user_dir / f"{filename}.md"

    if not filepath.exists():
        await message.answer(
            text=(
                "⚠️ Файл с таким названием не найден.\n"
                "Введите другое название заметки для объединения."
            )
        )
        return

    data = await state.get_data()
    if data["first_filepath"] == filepath:
        await message.answer(
            text=(
                "⚠️ Нельзя объединять одну и ту же заметку с самой собой.\n"
                "Введите название другой заметки."
            )
        )
        return

    await state.update_data(second_filepath=filepath)
    await state.set_state(MergeNotes.new_file)

    await message.answer(
        text=(
            "📂 Отлично! Теперь придумайте название для новой заметки, "
            "в которую будут объединены выбранные файлы."
        ),
        reply_markup=exit_kb(),
    )


@router.message(MergeNotes.second_file)
async def handle_invalid_merge_secondfile(message: types.Message):
    await message.answer(
        text=(
            "⚠️ Некорректные данные.\n"
            "Попробуйте ввести корректное название для новой заметки."
        ),
        reply_markup=exit_kb())


@router.message(MergeNotes.new_file, F.text)
async def handle_final_merge(message: types.Message, state: FSMContext):
    user_dir = ensure_user_dir(message.from_user.id)

    new_filename = sanitize_name(message.text.strip())
    new_filepath = user_dir / f"{new_filename}.md"

    data = await state.get_data()
    first_filepath = Path(data["first_filepath"])
    second_filepath = Path(data["second_filepath"])

    # читаем первый файл
    with open(first_filepath, encoding="utf-8") as f1:
        content1 = f1.readlines()[1:]  # без заголовка

    # считаем количество мыслей в первом файле
    count_first = sum(1 for line in content1 if line.startswith("## Мысль №"))

    # читаем второй файл
    with open(second_filepath, encoding="utf-8") as f2:
        lines2 = f2.readlines()[1:]

    # перенумеровываем второй файл
    updated_lines2 = []
    for line in lines2:
        if line.startswith("## Мысль №"):
            num = int(line.split("№")[1])
            line = f"## Мысль №{num + count_first}\n"
        updated_lines2.append(line)

    # пишем новый файл
    with open(new_filepath, "w", encoding="utf-8") as new_f:
        new_f.write(f"# {new_filename}\n\n")
        new_f.writelines(content1)
        new_f.writelines(updated_lines2)

    await message.answer(
        text=(
            f"🎉 Новая заметка успешно создана!\n"
            f"Файл <b>{new_filename}.md</b> объединяет выбранные заметки и готов к редактированию."
        ),
        reply_markup=exit_kb(),
    )
    await state.clear()
