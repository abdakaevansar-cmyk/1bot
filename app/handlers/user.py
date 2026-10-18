from __future__ import annotations

import inspect

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.database.repository import UserRepository
from app.keyboards.main_menu import get_main_menu_keyboard
from config import load_settings

router = Router()


async def handle_start_command(message: Message) -> bool:
    if message.from_user is None:
        return False

    settings = load_settings()
    repo = UserRepository(settings.database_url)
    await repo.init_db()
    await repo.get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
    )
    response = message.answer(
        "Welcome! I am your Telegram bot foundation.\n\n"
        "Use /menu to open the main menu, /help for commands, or /profile to view your data.",
        reply_markup=get_main_menu_keyboard(message.from_user.id in settings.admin_ids),
    )
    if inspect.isawaitable(response):
        await response
    await repo.close()
    return True


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message) -> None:
    await handle_start_command(message)


@router.message(Command(commands=["help"]))
async def cmd_help(message: Message) -> None:
    help_text = (
        "/start — welcome and create your record\n"
        "/help — show available commands\n"
        "/menu — open the main menu\n"
        "/profile — show your profile\n"
        "/settings — show settings\n"
        "/admin — admin panel for authorized users\n"
        "/cancel — cancel the current action"
    )
    await message.answer(help_text, reply_markup=get_main_menu_keyboard())


@router.message(Command(commands=["menu"]))
async def cmd_menu(message: Message) -> None:
    settings = load_settings()
    await message.answer("Main menu", reply_markup=get_main_menu_keyboard(message.from_user.id in settings.admin_ids))


@router.message(Command(commands=["profile"]))
async def cmd_profile(message: Message) -> None:
    if message.from_user is None:
        return

    repo = UserRepository(load_settings().database_url)
    await repo.init_db()
    user = await repo.get_user_by_id(message.from_user.id)
    await repo.close()

    if user is None:
        await message.answer("No profile found yet. Use /start first.")
        return

    username = user.username or "n/a"
    first_name = user.first_name or "n/a"
    last_name = user.last_name or "n/a"
    await message.answer(
        f"Your profile:\n\n"
        f"Telegram ID: {user.telegram_id}\n"
        f"Username: {username}\n"
        f"First name: {first_name}\n"
        f"Last name: {last_name}"
    )


@router.message(Command(commands=["settings"]))
async def cmd_settings(message: Message) -> None:
    await message.answer(
        "Settings are not yet configured for your business logic.\n"
        "You can extend this foundation with per-user preferences here.",
        reply_markup=get_main_menu_keyboard(),
    )


@router.message(Command(commands=["cancel"]))
async def cmd_cancel(message: Message) -> None:
    await message.answer("The current operation has been canceled.")


@router.callback_query(F.data == "menu")
async def cb_menu(callback: CallbackQuery) -> None:
    settings = load_settings()
    await callback.message.edit_text("Main menu", reply_markup=get_main_menu_keyboard(callback.from_user.id in settings.admin_ids))
    await callback.answer()


@router.callback_query(F.data == "profile")
async def cb_profile(callback: CallbackQuery) -> None:
    repo = UserRepository(load_settings().database_url)
    await repo.init_db()
    user = await repo.get_user_by_id(callback.from_user.id)
    await repo.close()

    if user is None:
        await callback.message.edit_text("No profile found yet. Use /start first.")
        await callback.answer()
        return

    lines = [
        "Your profile:",
        f"Telegram ID: {user.telegram_id}",
        f"Username: {user.username or 'n/a'}",
        f"First name: {user.first_name or 'n/a'}",
        f"Last name: {user.last_name or 'n/a'}",
    ]
    await callback.message.edit_text("\n".join(lines), reply_markup=get_main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "settings")
async def cb_settings(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "Settings are not yet configured for your business logic.\nYou can add user preferences here.",
        reply_markup=get_main_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "help")
async def cb_help(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "/start — welcome and create your record\n"
        "/help — show available commands\n"
        "/menu — open the main menu\n"
        "/profile — show your profile\n"
        "/settings — show settings\n"
        "/admin — admin panel for authorized users\n"
        "/cancel — cancel the current action",
        reply_markup=get_main_menu_keyboard(),
    )
    await callback.answer()


@router.message()
async def unknown_message(message: Message) -> None:
    await message.answer("I did not understand that. Try /help or /menu.")
