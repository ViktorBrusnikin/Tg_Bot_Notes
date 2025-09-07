from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.common_keyboards import exit_back_kb, abstract_kb_builder
from routers.work_w_notes.states import Notes
from tools.verification_number import verification_number

router = Router(name=__name__)


@router.message(Notes.abstract, Command('delete_thought'))
async def handle_command_delete(message: types.Message, state: FSMContext):
    await message.answer(
        text=(
            "🗑 Введите номер мысли, которую хотите удалить.\n\n"
            "🔹 Для выхода в главное меню — нажмите кнопку 'Главное меню'.\n"
            "🔹 Чтобы продолжить запись в текущей заметке — нажмите кнопку 'Вернуться'."
        ),
        reply_markup=exit_back_kb(),
    )
    await state.set_state(Notes.delete_thought)


@router.message(Command('delete_thought'))
async def handle_invalid_command_delete(message: types.Message):
    await message.answer(
        text=(
            "⚠️ Для начала выберите заметку, мысль в которой хотите удалить!\n"
            "Используйте команду /open для открытия существующей заметки или /create для создания новой."
        ),
    )


@router.message(Notes.delete_thought, F.text)
async def handle_delete_thought_state(message: types.Message, state: FSMContext):
    is_valid, number = await verification_number(message, state, message.text)

    if not is_valid:
        return

    data = await state.get_data()
    filepath = data.get("filepath")

    updated_lines = []
    current_number = 0

    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith("## Мысль №"):
            current_number += 1

            if current_number == number:
                # пропускаем удаляемую мысль
                i += 1
                while i < len(lines) and not lines[i].startswith("## Мысль №"):
                    i += 1
                continue
            else:
                # перенумеровываем оставшиеся мысли
                new_number = current_number - 1 if current_number > number else current_number
                line = f"## Мысль №{new_number}\n"

        updated_lines.append(line)
        i += 1

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

    await message.answer(
        text=(
            f"✅ Мысль №{number} успешно удалена 🗑\n\n"
            "Вы можете продолжать конспектировать свои мысли в текущей заметке."
        )
    )

    await message.answer(
        text="\n\nМожете продолжать конспектировать свои мысли",
        reply_markup=abstract_kb_builder()
    )

    await state.set_state(Notes.abstract)


@router.message(Notes.delete_thought)
async def handle_invalid_delete_thought_state(message: types.Message):
    await message.answer(
        text=(
            "⚠️ Некорректный ввод. Введите номер мысли цифрами.\n"
            "🔹 Для выхода в главное меню — кнопка 'Главное меню'.\n"
            "🔹 Чтобы вернуться к записи — кнопка 'Вернуться'."
        ),
        reply_markup=exit_back_kb(),
    )