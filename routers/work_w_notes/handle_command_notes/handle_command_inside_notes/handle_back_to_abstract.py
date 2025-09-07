from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from keyboards.common_keyboards import abstract_kb_builder
from routers.work_w_notes.states import Notes


router = Router(name=__name__)


back_to_abstract_filter = StateFilter(
    Notes.abstract,
    Notes.enumerate_notes,
    Notes.back_to_abstract,
    Notes.edit_note_begin,
    Notes.edit_note_end,
    Notes.show_thought,
    Notes.delete_thought,
)



@router.message(back_to_abstract_filter, F.text == "Вернуться")
async def handle_back_to_abstract(message: types.Message, state: FSMContext):
    await message.answer(
        text="Можете продолжать запись",
        reply_markup=abstract_kb_builder(),
    )
    await state.set_state(Notes.abstract)