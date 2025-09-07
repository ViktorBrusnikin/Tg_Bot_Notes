from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.common_keyboards import exit_back_kb, abstract_kb_builder
from routers.work_w_notes.states import Notes
from tools.verification_number import verification_number

router = Router(name=__name__)


@router.message(Notes.abstract, Command('edit'))
async def handle_command_note(message: types.Message, state: FSMContext):
    data = await state.get_data()
    filepath = data.get("filepath")

    flag = False
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("## Мысль №"):
                flag = True
                break

    if not flag:
        await message.answer(
            text=(
                "⚠️ Заметка пустая. Сначала добавьте текст, чтобы можно было редактировать мысли."
            )
        )
        return

    await message.answer(
        text=(
            "✏️ Введите номер главы (Мысли), которую хотите отредактировать.\n\n"
            "🔹 Для выхода в главное меню — нажмите кнопку 'Главное меню'.\n"
            "🔹 Чтобы продолжить запись в текущей заметке — нажмите кнопку 'Вернуться'."
        ),
        reply_markup=exit_back_kb(),
    )
    await state.set_state(Notes.edit_note_begin)


@router.message(Command('edit'))
async def handle_invalid_command_note(message: types.Message):
    await message.answer(
        text=(
            "⚠️ Перед редактированием выберите заметку командой /open или создайте новую с помощью /create."
        )
    )


@router.message(Notes.edit_note_begin, F.text)
async def handle_edit_note_begin_state(message: types.Message, state: FSMContext):
    is_valid, number = await verification_number(message, state, message.text)

    if not is_valid:
        return

    await state.update_data(edit_number=number)
    await message.answer(
        text=(
            f"✏️ Введите новый текст для мысли №{number}.\n\n"
            "🔹 Для выхода в главное меню — нажмите кнопку 'Главное меню'.\n"
            "🔹 Чтобы продолжить запись — нажмите кнопку 'Вернуться'."
        ),
        reply_markup=exit_back_kb(),
    )
    await state.set_state(Notes.edit_note_end)


@router.message(Notes.edit_note_begin)
async def handle_invalid_edit_note_begin_state(message: types.Message):
    await message.answer(
        text=(
            "⚠️ Некорректный ввод. Пожалуйста, введите номер мысли цифрами.\n"
            "🔹 Для выхода в главное меню — кнопка 'Главное меню'.\n"
            "🔹 Чтобы вернуться к записи — кнопка 'Вернуться'."
        ),
        reply_markup=exit_back_kb(),
    )


@router.message(Notes.edit_note_end, F.text)
async def handle_edit_note_end_state(message: types.Message, state: FSMContext):
    data = await state.get_data()

    number = data.get("edit_number")
    filepath = data.get("filepath")
    new_thought = message.text.strip()

    if not filepath:
        await message.answer(
            text=(
                "⚠️ Файл не найден.\n"
                "Сначала откройте существующую заметку командой /open или создайте новую с помощью /create, "
                "чтобы продолжить редактирование."
            )
        )
        await state.set_state(Notes.abstract)
        return

    updated_lines = []
    replaced = False

    with open(filepath, encoding='utf-8') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith(f"## Мысль №{number}"):
            # добавляем новый блок
            updated_lines.append(f"## Мысль №{number}\n{new_thought}\n\n")
            replaced = True
            # пропускаем старую мысль
            i += 1
            while i < len(lines) and not lines[i].startswith("## Мысль №"):
                i += 1
            continue
        updated_lines.append(line)
        i += 1

    if replaced:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(updated_lines)
        await message.answer(
            text=(
                f"✅ Мысль №{number} успешно обновлена!\n\n"
                "Теперь вы можете продолжать конспектировать свои мысли."
            )
        )
    else:
        await message.answer(
            text=(
                f"⚠️ Мысль №{number} не найдена 😕\n"
                "Проверьте номер и попробуйте снова."
            )
        )

    await message.answer(
        text="\n\nМожете продолжать конспектировать свои мысли",
        reply_markup=abstract_kb_builder(),
    )

    await state.set_state(Notes.abstract)


@router.message(Notes.edit_note_end)
async def handle_invalid_edit_note_end_state(message: types.Message):
    await message.answer(
        text=(
            "⚠️ Вы ввели некорректные данные! Используйте только текст.\n\n"
            "🔹 Для выхода в главное меню — нажмите кнопку 'Главное меню'.\n"
            "🔹 Чтобы продолжить запись — нажмите кнопку 'Вернуться'."
        ),
        reply_markup=exit_back_kb(),
    )