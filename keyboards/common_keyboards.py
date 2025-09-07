from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_kb_builder() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text='Главное меню')
    builder.button(text="/help")
    builder.adjust(1)
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def menu_kb_builder() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="/create")
    builder.button(text="/open")
    builder.button(text="/merge")
    builder.button(text="/delete_note")
    builder.button(text="/all")
    builder.adjust(2,2,1)
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def abstract_kb_builder() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text='/change')
    builder.button(text='/view')
    builder.button(text='/note')
    builder.button(text='/edit')
    builder.button(text='/delete_thought')
    builder.button(text='Главное меню')
    builder.adjust(1, 2, 2, 1)
    return builder.as_markup(
        resize_keyboard=True,
    )


def exit_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text='Главное меню')
    return builder.as_markup(
        resize_keyboard=True,
    )


def exit_back_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text='Вернуться')
    builder.button(text='Главное меню')
    builder.adjust(1)
    return builder.as_markup(
        resize_keyboard=True,
    )