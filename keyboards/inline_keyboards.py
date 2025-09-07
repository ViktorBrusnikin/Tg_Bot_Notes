from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


send_file = "send_file"
send_text = "send_text"


def view_inline_kb_builder() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Исходный файл",
        callback_data=send_file,
    )
    builder.button(
        text="Содержимое файла",
        callback_data=send_text,
    )
    builder.adjust(2)
    return builder.as_markup()