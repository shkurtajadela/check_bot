from aiogram import Dispatcher

from bot.handlers.main_handlers import register_main_handlers, register_commands
from bot.handlers.create_check_handlers import register_create_check_handlers
from bot.handlers.add_to_check_handlers import register_add_to_check_handlers
from bot.handlers.pay_check_handlers import register_pay_check_handlers
from bot.handlers.my_checks_handlers import register_my_checks_handlers
from bot.handlers.notification_handlers import register_notification_handlers


def register_handlers(dp: Dispatcher) -> None:
    register_commands(dp=dp)
    register_notification_handlers(dp=dp)
    register_create_check_handlers(dp=dp)
    register_add_to_check_handlers(dp=dp)
    register_pay_check_handlers(dp=dp)
    register_my_checks_handlers(dp=dp)
    register_main_handlers(dp=dp)


