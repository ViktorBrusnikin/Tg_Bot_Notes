from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.common_keyboards import exit_back_kb
from keyboards.inline_keyboards import (
    view_inline_kb_builder,
    send_file,
    send_text
)
from routers.work_w_notes.states import Notes
from tools.chunk_text import chunk_text

router = Router(name=__name__)


@router.message(Notes.abstract, Command('view'))
async def handle_command_view(message: types.Message, state: FSMContext):
    await message.answer(
        text=(
            "👀 Выберите способ отображения содержимого файла:\n"
            "• Отправить весь файл как документ\n"
            "• Отправить содержимое как текст в сообщениях"
        ),
        reply_markup=view_inline_kb_builder()
    )
    await message.answer(
        text=(
            "🔙 Чтобы вернуться к конспектированию, используйте меню ниже."
        ),
        reply_markup=exit_back_kb()
    )

    await state.set_state(Notes.enumerate_notes)

@router.message(Command('view'))
async def handle_command_view(message: types.Message):
    await message.answer(
        text=(
            "⚠️ Вы пока не открыли ни одну заметку.\n"
            "Сначала откройте существующий файл командой /open или создайте новый с помощью /create."
        )
    )


@router.message(Notes.enumerate_notes)
async def handle_error_answer_in_view(message: types.Message):
    await message.answer(
        text=(
            "⚠️ Пожалуйста, используйте кнопки ниже для выбора действия.\n"
            "🔹 Чтобы вернуться к конспектированию — нажмите 'Вернуться'.\n"
            "🔹 Чтобы вернуться в главное меню — нажмите 'Главное меню'."
        ),
        reply_markup=exit_back_kb(),
    )

@router.callback_query(F.data == send_file)
async def handle_cb_send_file(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    filepath = data.get("filepath")

    if not filepath:
        await callback.answer(
            text=(
                "❌ Ошибка: файл не найден.\n"
                "Попробуйте снова открыть файл или создайте новую заметку."
            )
        )
        # Если файл не найден, отправляем делать новый
        await state.set_state(Notes.create_note)
        return

    file = FSInputFile(filepath)  # путь к твоему .md файлу
    await callback.message.answer_document(file, caption="📄 Вот твой Markdown файл с заметками!")

    await callback.answer()


@router.callback_query(F.data == send_text)
async def handle_cb_send_file(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    filepath = data.get("filepath")

    if not filepath:
        await callback.answer(
            text=(
                "❌ Ошибка: файл не найден.\n"
                "Попробуйте снова открыть файл или создайте новую заметку."
            )
        )
        # Если файл не найден, отправляем делать новый
        await state.set_state(Notes.create_note)
        return

    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    await callback.message.answer(
        text="✏️ Содержимое заметки:"
    )

    for chunk in chunk_text(content):
        await callback.message.answer(
            text=chunk,
            parse_mode=ParseMode.MARKDOWN
        )

    await callback.answer()