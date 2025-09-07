from aiogram import types
from aiogram.fsm.context import FSMContext


async def verification_number(
    message: types.Message,
    state: FSMContext,
    answer: str
) -> tuple[bool, int | None]:
    try:
        number = int(answer)
        if number <= 0:
            raise ValueError
    except ValueError:
        await message.answer(
            text=(
                "⚠️ Некорректный ввод. Пожалуйста, введите номер мысли цифрами.\n"
                "🔹 Для выхода в главное меню — кнопка 'Главное меню'.\n"
                "🔹 Чтобы вернуться к записи — кнопка 'Вернуться'."
            )
        )
        return False, None

    data = await state.get_data()
    filepath = data.get("filepath")

    with open(filepath, encoding="utf-8") as f:
        for line in f:
            if line.startswith(f"## Мысль №{number}"):
                return True, number

    await message.answer(
        text=(f"🤔 Мысль №{number} отсутствует в заметке. Попробуйте другой номер или начните новую запись.")
    )

    return False, number