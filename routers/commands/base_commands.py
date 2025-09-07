from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils import markdown

from keyboards.common_keyboards import start_kb_builder

router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start(message: types.Message, state: FSMContext):
    await state.clear()
    text = f"""
Здравствуйте, {markdown.hbold(message.from_user.full_name)} 👋  
Я — бот Notion, помогу вам вести заметки.  

👉 Чтобы начать работу — нажмите кнопку «Главное меню».  

👉 Чтобы увидеть список команд — нажмите «help» или введите /help.  
"""
    await message.answer(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=start_kb_builder(),
    )


@router.message(Command('help'))
async def handle_help(message: types.Message, state: FSMContext):
    await state.clear()
    text = f"""
Вот список команд, которые вы можете использовать:

📌 Основные команды:
/help — показать справку

🗂 Работа с заметками:
/change — перенести запись в другой файл
/merge — объединить два файла в один новый
/open — открыть существующий файл
/create — создать новый файл
/all — вывести список файлов

📝 Работа внутри заметок:
/view — показать всё содержимое заметки + отправить файл
/note — показать конкретную мысль
/edit — отредактировать мысль
/delete — удалить конкретную мысль
"""
    await message.answer(
        text=text,
        reply_markup=ReplyKeyboardRemove(),
    )

