from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.database.repository import UserRepository
from app.keyboards.main_menu import get_admin_menu_keyboard, get_main_menu_keyboard
from config import load_settings

router = Router()


def is_admin(chat_id: int) -> bool:
    settings = load_settings()
    return chat_id in settings.admin_ids


@router.message(Command(commands=["admin"]))
async def cmd_admin(message: Message) -> None:
    if message.from_user is None:
        return
    if not is_admin(message.from_user.id):
        await message.answer("Access denied: this command is reserved for administrators.")
        return

    repo = UserRepository(load_settings().database_url)
    await repo.init_db()
    total_users = await repo.count_users()
    await repo.close()

    await message.answer(
        f"Admin panel\n\nRegistered users: {total_users}\n\nUse the admin menu to inspect activity.",
        reply_markup=get_admin_menu_keyboard(),
    )


@router.callback_query(F.data == "admin")
async def cb_admin(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return

    repo = UserRepository(load_settings().database_url)
    await repo.init_db()
    total_users = await repo.count_users()
    await repo.close()

    await callback.message.edit_text(
        f"Admin panel\n\nRegistered users: {total_users}\n\nUse the admin menu to inspect activity.",
        reply_markup=get_admin_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "admin_stats")
async def cb_admin_stats(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return

    repo = UserRepository(load_settings().database_url)
    await repo.init_db()
    total_users = await repo.count_users()
    await repo.close()

    await callback.message.edit_text(
        f"Statistics\n\nTotal users: {total_users}\nAdmin IDs: {', '.join(str(x) for x in load_settings().admin_ids)}",
        reply_markup=get_admin_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "admin_users")
async def cb_admin_users(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("Access denied", show_alert=True)
        return

    repo = UserRepository(load_settings().database_url)
    await repo.init_db()
    users = await repo.list_users(limit=10)
    await repo.close()

    if not users:
        await callback.message.edit_text("No registered users yet.", reply_markup=get_admin_menu_keyboard())
        await callback.answer()
        return

    lines = ["Recent users:"]
    for user in users:
        name = user.username or user.first_name or "unknown"
        lines.append(f"- {user.telegram_id} ({name})")

    await callback.message.edit_text("\n".join(lines), reply_markup=get_admin_menu_keyboard())
    await callback.answer()
