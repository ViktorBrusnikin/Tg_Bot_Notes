from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.common_keyboards import exit_back_kb, abstract_kb_builder
from routers.work_w_notes.states import Notes
from tools.verification_number import verification_number

router = Router(name=__name__)


@router.message(Notes.abstract, Command('note'))
async def handle_command_note(message: types.Message, state: FSMContext):
    await message.answer(
        text=(
            "📝 Введите номер главы (Мысли), которую хотите просмотреть.\n\n"
            "🔹 Для выхода в главное меню — нажмите кнопку 'Главное меню'.\n"
            "🔹 Чтобы продолжить запись в текущей заметке — нажмите кнопку 'Вернуться'."
        ),
        reply_markup=exit_back_kb(),
    )
    await state.set_state(Notes.show_thought)


@router.message(Command('note'))
async def handle_invalid_command_note(message: types.Message):
    await message.answer(
        text=(
            "⚠️ Сначала откройте существующую заметку командой /open или создайте новую с помощью /create.\n"
            "Только после этого можно просматривать отдельные мысли."
        )
    )


@router.message(Notes.show_thought, F.text)
async def handle_state_show_thought(message: types.Message, state: FSMContext):
    is_valid, number = await verification_number(message, state, message.text)

    if not is_valid:
        return

    data = await state.get_data()
    filepath = data.get("filepath")

    content_lines = []
    capture = False


    with open(filepath, encoding="utf-8") as f:
        for line in f:
            if line.startswith(f"## Мысль №{number}"):
                capture = True
                content_lines.append(line)  # добавляем сам заголовок
                continue
            if capture:
                if line.startswith("## Мысль №"):  # наткнулись на следующий заголовок
                    break
                content_lines.append(line)

    content = "".join(content_lines).strip()

    await message.answer(
        text=f"✏️ Содержимое выбранной мысли:\n\n{content}" if content else f"ℹ️ Мысль №{number} пока пустая.\nВы можете добавить текст в эту мысль прямо сейчас.",
        parse_mode=ParseMode.MARKDOWN,
    )

    await message.answer(
        text="Вы можете продолжать конспектировать свои мысли в текущей заметке.",
        reply_markup=abstract_kb_builder(),
    )

    await state.set_state(Notes.abstract)


@router.message(Notes.show_thought)
async def handle_invalid_state_show_thought(message: types.Message):
    await message.answer(
        text=(
            "⚠️ Некорректный ввод. Пожалуйста, введите номер мысли цифрами."
        )
    )