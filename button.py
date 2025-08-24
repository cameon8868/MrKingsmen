from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F, Dispatcher, html
from aiogram.fsm.context import FSMContext

# Product data dictionaries
shirts_data = {
    "item1": {"name": "Классическая белая рубашка", "price": "3500 руб.", "description": "Идеально подходит для деловых встреч.", "image": "https://i.imgur.com/example_shirt1.jpg"},
    "item2": {"name": "Льняная рубашка в полоску", "price": "4200 руб.", "description": "Легкая и стильная для летнего сезона.", "image": "https://i.imgur.com/example_shirt2.jpg"}
}

jackets_data = {
    "item1": {"name": "Синий шерстяной пиджак", "price": "12000 руб.", "description": "Элегантный пиджак для офиса и торжеств.", "image": "https://i.imgur.com/example_jacket1.jpg"},
    "item2": {"name": "Легкий блейзер из хлопка", "price": "8500 руб.", "description": "Универсальный вариант для повседневного образа.", "image": "https://i.imgur.com/example_jacket2.jpg"}
}

shoes_data = {
    "item1": {"name": "Классические кожаные оксфорды", "price": "9800 руб.", "description": "Изысканная обувь для официальных мероприятий.", "image": "https://i.imgur.com/example_shoe1.jpg"},
    "item2": {"name": "Мокасины из замши", "price": "7200 руб.", "description": "Комфортная обувь для отдыха и прогулок.", "image": "https://i.imgur.com/example_shoe2.jpg"}
}

pants_data = {
    "item1": {"name": "Классические шерстяные брюки", "price": "6500 руб.", "description": "Удобные и стильные брюки для любого случая.", "image": "https://i.imgur.com/example_pants1.jpg"},
    "item2": {"name": "Чинос из хлопка", "price": "4800 руб.", "description": "Повседневные брюки для современного гардероба.", "image": "https://i.imgur.com/example_pants2.jpg"}
}

def get_start_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Рубашки", callback_data="shirts")],
        [InlineKeyboardButton(text="Пиджаки", callback_data="jackets")],
        [InlineKeyboardButton(text="Обувь", callback_data="shoes")],
        [InlineKeyboardButton(text="Брюки", callback_data="other")]
    ])
    return keyboard

def get_main_reply_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Профиль")],
        [KeyboardButton(text="Купить товар")],
        [KeyboardButton(text="Получить скидку")]
    ], resize_keyboard=True)
    return keyboard

def get_suggestion_keyboard(category: str, current_index: int, total_items: int) -> InlineKeyboardMarkup:
    buttons = []

    # Navigation buttons
    if current_index > 0:
        buttons.append([InlineKeyboardButton(text="Назад", callback_data=f"prev_item_{category}_{current_index}")])
    if current_index < total_items - 1:
        buttons.append([InlineKeyboardButton(text="Вперед", callback_data=f"next_item_{category}_{current_index}")])

    # Suggestion buttons
    buttons.append([InlineKeyboardButton(text="В корзину", callback_data="add_to_cart")],)

    # Back to categories button
    buttons.append([InlineKeyboardButton(text="← Назад к категориям", callback_data="back_to_categories")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_consent_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Согласен", callback_data="agree_privacy")],
        [InlineKeyboardButton(text="Не согласен", callback_data="disagree_privacy")]
    ])
    return keyboard

async def register_callback_handlers(dp: Dispatcher):
    @dp.callback_query(F.data == "shirts")
    async def process_shirts_button(callback: CallbackQuery):
        category = "shirts"
        products = shirts_data
        current_index = 0
        
        if products:
            item_data = products[list(products.keys())[current_index]]
            caption = f"<b>{item_data['name']}</b>\n"
            caption += f"Цена: {item_data['price']}\n"
            caption += f"Описание: {item_data['description']}"

            reply_markup = get_suggestion_keyboard(category, current_index, len(products))
            if item_data.get('image'):
                await callback.message.answer_photo(photo=item_data['image'], caption=caption, reply_markup=reply_markup, parse_mode="html")
            else:
                await callback.message.answer(text=caption, reply_markup=reply_markup, parse_mode="html")
        else:
            await callback.message.answer(text="В этой категории пока нет товаров.")

        await callback.answer()

    @dp.callback_query(F.data == "jackets")
    async def process_jackets_button(callback: CallbackQuery):
        category = "jackets"
        products = jackets_data
        current_index = 0

        if products:
            item_data = products[list(products.keys())[current_index]]
            caption = f"<b>{item_data['name']}</b>\n"
            caption += f"Цена: {item_data['price']}\n"
            caption += f"Описание: {item_data['description']}"

            reply_markup = get_suggestion_keyboard(category, current_index, len(products))
            if item_data.get('image'):
                await callback.message.answer_photo(photo=item_data['image'], caption=caption, reply_markup=reply_markup, parse_mode="html")
            else:
                await callback.message.answer(text=caption, reply_markup=reply_markup, parse_mode="html")
        else:
            await callback.message.answer(text="В этой категории пока нет товаров.")

        await callback.answer()

    @dp.callback_query(F.data == "shoes")
    async def process_shoes_button(callback: CallbackQuery):
        category = "shoes"
        products = shoes_data
        current_index = 0

        if products:
            item_data = products[list(products.keys())[current_index]]
            caption = f"<b>{item_data['name']}</b>\n"
            caption += f"Цена: {item_data['price']}\n"
            caption += f"Описание: {item_data['description']}"

            reply_markup = get_suggestion_keyboard(category, current_index, len(products))
            if item_data.get('image'):
                await callback.message.answer_photo(photo=item_data['image'], caption=caption, reply_markup=reply_markup, parse_mode="html")
            else:
                await callback.message.answer(text=caption, reply_markup=reply_markup, parse_mode="html")
        else:
            await callback.message.answer(text="В этой категории пока нет товаров.")

        await callback.answer()

    @dp.callback_query(F.data == "other")
    async def process_other_button(callback: CallbackQuery):
        category = "other"
        products = pants_data
        current_index = 0

        if products:
            item_data = products[list(products.keys())[current_index]]
            caption = f"<b>{item_data['name']}</b>\n"
            caption += f"Цена: {item_data['price']}\n"
            caption += f"Описание: {item_data['description']}"

            reply_markup = get_suggestion_keyboard(category, current_index, len(products))
            if item_data.get('image'):
                await callback.message.answer_photo(photo=item_data['image'], caption=caption, reply_markup=reply_markup, parse_mode="html")
            else:
                await callback.message.answer(text=caption, reply_markup=reply_markup, parse_mode="html")
        else:
            await callback.message.answer(text="В этой категории пока нет товаров.")

        await callback.answer()

    @dp.callback_query(F.data.startswith("prev_item_"))
    @dp.callback_query(F.data.startswith("next_item_"))
    async def navigate_items_button(callback: CallbackQuery, state: FSMContext):
        parts = callback.data.split('_')
        action = parts[0]
        category = parts[2]
        current_index = int(parts[3])
        
        products_data = {
            "shirts": shirts_data,
            "jackets": jackets_data,
            "shoes": shoes_data,
            "other": pants_data
        }
        products = products_data.get(category)

        if not products:
            await callback.message.answer(text="Произошла ошибка: категория не найдена.", parse_mode="html")
            await callback.answer()
            return

        total_items = len(products)
        new_index = current_index

        if action == "prev_item":
            new_index = max(0, current_index - 1)
        elif action == "next_item":
            new_index = min(total_items - 1, current_index + 1)

        if new_index == current_index:
            await callback.answer("Вы уже на первом/последнем товаре в этой категории.")
            return

        item_data = products[list(products.keys())[new_index]]
        caption = f"<b>{item_data['name']}</b>\n"
        caption += f"Цена: {item_data['price']}\n"
        caption += f"Описание: {item_data['description']}"

        reply_markup = get_suggestion_keyboard(category, new_index, total_items)
        if item_data.get('image'):
            await callback.message.answer_photo(photo=item_data['image'], caption=caption, reply_markup=reply_markup, parse_mode="html")
        else:
            await callback.message.answer(text=caption, reply_markup=reply_markup, parse_mode="html")
        await callback.answer()

    @dp.callback_query(F.data == "add_to_cart")
    async def add_to_cart_button(callback: CallbackQuery):
        # In a real bot, you would add the selected item to a user's cart here
        await callback.message.answer(text="Товар добавлен в корзину!", parse_mode="html")
        await callback.answer()

    @dp.callback_query(F.data == "back_to_categories")
    async def process_back_to_categories_button(callback: CallbackQuery):
        keyboard = get_start_keyboard()
        await callback.message.answer(text="Что хотите приобрести?", reply_markup=keyboard, parse_mode="html")
        await callback.answer()
