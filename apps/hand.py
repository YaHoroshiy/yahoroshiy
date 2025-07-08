import asyncio
from aiogram import Bot,Dispatcher,F,Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart,Command
from apps.key import main_kb,categories,items# Импортируем обе клавиатуры
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
import apps.database.requests as rq
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from apps.database.requests import create_support_ticket, get_user_by_tg_id



router = Router()
@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Привет', reply_markup=main_kb)
    await message.reply('Как дела')
@router.message(F.text == 'Каталог')
async def catalog(message :Message):
    await message.answer('Выберите категорию товара',reply_markup=await categories())
@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    category_id = callback.data.split('_')[1]
    await callback.message.answer('Выберите товар', reply_markup=await items(category_id))
@router.callback_query(F.data.startswith('item'))
async def category(callback:CallbackQuery):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await callback.answer('Вы выбрали товар')
    await callback.message.answer(f'Название:{item_data.name}Награда:{item_data.reward}',
                                  reply_markup=await items(callback.data))
@router.callback_query(F.data == 'to_main')
async def back_to_main(callback: CallbackQuery):
    await callback.message.delete()  
    await callback.message.answer(
        "Вы вернулись в главное меню",
        reply_markup=main_kb
    )
    await callback.answer()
@router.callback_query(F.data == 'back_to_categories')
async def back_to_categories(callback: CallbackQuery):
    await callback.message.delete()  
    await callback.message.answer(
        "Выберите категорию товара",
        reply_markup=await categories()
    )
    await callback.answer()
class SupportState(StatesGroup):
    waiting_for_support_message = State()

@router.callback_query(F.data == 'TP_room')
async def TP_room(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "✍️ Напишите ваш вопрос для техподдержки. Мы ответим вам как можно скорее.\n"
        "Для отмены используйте /cancel"
    )
    await state.set_state(SupportState.waiting_for_support_message)
    await callback.answer()
@router.message(Command("cancel"))
async def cancel_support(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == SupportState.waiting_for_support_message:
        await state.clear()
        await message.answer(
            "❌ Режим техподдержки отменен.",
            reply_markup=await categories()
        )
    else:
        # Если команда /cancel вызвана не в режиме поддержки
        await message.answer(
            "Нечего отменять. Вы в главном меню.",
            reply_markup=await categories()
        )

# Этот обработчик должен быть ПОСЛЕ обработчика команды /cancel
@router.message(SupportState.waiting_for_support_message)
async def process_support_message(message: Message, state: FSMContext, bot: Bot):
    # Проверяем, не является ли сообщение командой
    if message.text.startswith('/'):
        return  # Игнорируем команды
        
    SUPPORT_CHAT_ID = 7268834861  # Ваш ID
    
    try:
        user = await get_user_by_tg_id(message.from_user.id)
        if not user:
            await message.answer("❌ Ошибка: пользователь не найден.")
            await state.clear()
            return

        ticket = await create_support_ticket(user.id, message.text)
        
        if not ticket:
            await message.answer("❌ Не удалось создать обращение.")
            await state.clear()
            return

        user_info = f"ID: {message.from_user.id}\nИмя: {message.from_user.full_name}"
        if message.from_user.username:
            user_info += f"\nUsername: @{message.from_user.username}"
        
        await bot.send_message(
            SUPPORT_CHAT_ID,
            f"🚨 Новое обращение #{ticket.id}\n\n"
            f"👤 {user_info}\n"
            f"🕒 {ticket.created_at}\n\n"
            f"📄 {message.text}"
        )
        
        await message.answer(
            "✅ Ваше сообщение отправлено в техподдержку.\n"
            f"Номер обращения: #{ticket.id}",
            reply_markup=await categories()
        )
    
    except Exception as e:
        print(f"Ошибка: {e}")
        await message.answer(
            "❌ Произошла ошибка при отправке.",
            reply_markup=await categories()
        )
    
    finally:
        await state.clear()