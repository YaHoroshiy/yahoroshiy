from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from apps.database.requests import get_categories
from aiogram.utils.keyboard import InlineKeyboardBuilder
from apps.database.requests import get_category_item


main_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Каталог')]],  # Исправлено на KeyboardButton
    input_field_placeholder='Выберите пункт меню...'
)

async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()

    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
        keyboard.add(InlineKeyboardButton(text='Тех поддержка',callback_data='TP_room',resize_keyboard=True))

    return keyboard.adjust(2).as_markup()

async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()

    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"item_{item.id}"))
    
    # Сначала добавляем все кнопки товаров, затем настраиваем их расположение
    keyboard.adjust(2)
    
    # Добавляем остальные кнопки
    keyboard.row(InlineKeyboardButton(text='Категории', callback_data='back_to_categories',resize_keyboard=True))
    keyboard.row(InlineKeyboardButton(text='Тех поддержка', callback_data='TP_room',resize_keyboard=True))
    keyboard.row(InlineKeyboardButton(text='❌ Отмена', callback_data='to_main',resize_keyboard=True))
    
    return keyboard.as_markup()