import os
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from keyboards.common_keyboards import abstract_kb_builder
from routers.work_w_notes.states import Notes

router = Router(name=__name__)


@router.message(Notes.abstract, F.text)
async def handle_abstract_state(message: types.Message, state: FSMContext):
    # Достаём путь до созданного файла
    data = await state.get_data()
    filepath = data.get("filepath")

    if not filepath:
        await message.answer("Ошибка. Файл не найден, попробуйте снова")
        # Если файл не найден, отправляем делать новый
        await state.set_state(Notes.create_note)
        return

    # 1. Определяем, сколько мыслей уже есть в файле
    last_index = 0
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("## Мысль №"):
                    try:
                        num = int(line.replace("## Мысль №", "").strip())
                        last_index = max(last_index, num)
                    except ValueError:
                        pass

    with open(filepath, 'a', encoding='utf-8') as f:
        paragraphs = message.text.split("\n\n")
        for p in paragraphs:
            lines = p.split("\n")
            joined = "<br>".join(lines)
            last_index += 1  # увеличиваем последний индекс
            f.write(f"## Мысль №{last_index}\n{joined}\n\n")

    await message.answer(
        text="Записал! Можете продолжать вводить заметки!",
        reply_markup=abstract_kb_builder(),
    )


@router.message(Notes.abstract)
async def handle_abstract_state(message: types.Message):
    await message.answer(
        text="Записать можно только текст...",
        reply_markup=abstract_kb_builder(),
    )