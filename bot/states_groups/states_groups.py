from aiogram.dispatcher.filters.state import StatesGroup, State


class StartStatesGroup(StatesGroup):
    start = State()


class CheckCreationStatesGroup(StatesGroup):
    photo = State()
    description = State()
    summ = State()
    summ_own = State()
    requisites = State()


class MainMenuStatesGroup(StatesGroup):
    main_menu = State()


class CheckSubmissionStatesGroup(StatesGroup):
    check_submission = State()


class AddToCheckStatesGroup(StatesGroup):
    add_to_check = State()


class PayCheckStatesGroup(StatesGroup):
    pay_check = State()
    summ_to_pay = State()
    summ_paid = State()


class InfoCheckStatesGroup(StatesGroup):
    choose_check = State()
    delete_notify_check = State()
    delete_confirm = State()