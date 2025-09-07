from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils import markdown

from keyboards.common_keyboards import menu_kb_builder

router = Router(name=__name__)


@router.message(F.text == "Главное меню")
async def handle_command_menu(message: types.Message, state: FSMContext):
    await state.clear()
    text = (
        f"{markdown.hbold('Главное меню')}\n\n"
        f"Здесь вы можете создавать и управлять своими заметками. "
        f"Каждая заметка может содержать несколько {markdown.hitalic('мыслей')} — небольших блоков текста, "
        "каждый из которых отделён от других и представляет отдельную идею.\n\n\n"
        "📌 Чтобы создать новую заметку — нажмите кнопку «create» или используйте команду /create.\n\n"
        "📂 Чтобы открыть существующую заметку — кнопку «open» или команду /open.\n\n"
        "📝 Чтобы посмотреть список всех заметок — кнопку «all» или команду /all.\n\n"
        "🔗 Чтобы объединить две заметки в одну — кнопку «merge» или команду /merge.\n\n"
        "🗑 Чтобы удалить заметку — кнопку «delete_note» или команду /delete_note."
    )
    await message.answer(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=menu_kb_builder(),
    )
