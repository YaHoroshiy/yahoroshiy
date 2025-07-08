from apps.database.models import async_session
from apps.database.models import User,Category,Item
from sqlalchemy import select,update,delete,desc

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))
async def get_category_item(category_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.category == category_id))

async def get_item(item_id):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == item_id))
# Добавьте в requests.py
from datetime import datetime
from apps.database.models import SupportTicket

async def create_support_ticket(user_id: int, message: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_id))
        if user:
            ticket = SupportTicket(
                user_id=user.id,
                message=message,
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            session.add(ticket)
            await session.commit()
            return ticket
        return None

async def get_user_by_tg_id(tg_id: int):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))
async def create_support_ticket(user_id: int, message: str):
    async with async_session() as session:
        try:
            ticket = SupportTicket(
                user_id=user_id,
                message=message,
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            session.add(ticket)
            await session.commit()
            await session.refresh(ticket)  # Обновляем объект, чтобы получить ID
            return ticket
        except Exception as e:
            print(f"Ошибка при создании тикета: {e}")
            await session.rollback()
            return None