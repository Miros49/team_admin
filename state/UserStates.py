from aiogram.fsm.state import default_state, State, StatesGroup


class UserState(StatesGroup):
    create_profile_1 = State()
    create_profile_2 = State()
    create_profile_3 = State()
    create_profile_4 = State()
    create_profile_5 = State()
    create_profile_6 = State()
    create_profile_7 = State()
    checker_enter_link: State = State()
