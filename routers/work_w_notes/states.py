from aiogram.fsm.state import StatesGroup, State


class Notes(StatesGroup):
    create_note = State()
    open_note = State()
    abstract = State()
    choose_note = State()
    enumerate_notes = State()
    edit_note_begin = State()
    edit_note_end = State()
    show_thought = State()
    delete_thought = State()
    delete_note = State()
    back_to_abstract = State()


class MergeNotes(StatesGroup):
    first_file = State()
    second_file = State()
    new_file = State()