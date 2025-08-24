import asyncio
import qrcode
import logging
from aiogram import Bot, Dispatcher, html, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from button import get_start_keyboard, register_callback_handlers, get_main_reply_keyboard, get_consent_keyboard
from db import init_db, get_user_info, save_user_info, get_all_user_ids, update_user_consent

# Configure logging
logging.basicConfig(level=logging.INFO)

# Replace with your actual bot token
BOT_TOKEN = "7559529190:AAHQE5Wim83zkzgV79SY9FvP8lU_r0ftM34"

# Define states for our conversation
class Form(StatesGroup):
    waiting_for_phone_number = State()
    waiting_for_address = State()
    waiting_for_consent = State()

# Background task for sending push notifications
async def send_push_notifications(bot: Bot):
    while True:
        await asyncio.sleep(600)  # Wait for 10 minutes (600 seconds)
        user_ids = get_all_user_ids()
        for user_id in user_ids:
            try:
                await bot.send_message(user_id, "Это push уведомление")
                logging.info(f"Push notification sent to user {user_id}")
            except Exception as e:
                logging.error(f"Failed to send push notification to user {user_id}: {e}")

# Main function
async def main() -> None:
    init_db()
    # Initialize Bot and Dispatcher
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    
    # All handlers should be async
    @dp.message(CommandStart())
    async def command_start_handler(message: Message, state: FSMContext) -> None:
        user_id = message.from_user.id
        address, phone_number, has_agreed_privacy = get_user_info(user_id)
        
        if not has_agreed_privacy:
            privacy_text = (
                "Приветствую! Прежде чем начать пользоваться ботом, "
                "нам необходимо ваше согласие на обработку персональных данных. "
                "Мы собираем ваш номер телефона и адрес для оказания услуг. "
                "Ознакомьтесь с нашей политикой конфиденциальности. "
                "Вы согласны на обработку ваших персональных данных?"
            )
            await message.answer(privacy_text, reply_markup=get_consent_keyboard())
            await state.set_state(Form.waiting_for_consent)
            return

        if not phone_number:
            await message.answer("Пожалуйста, введите ваш номер телефона (начиная с +7):")
            await state.set_state(Form.waiting_for_phone_number)
        elif not address: # Only ask for address if phone number is present
            await message.answer("Пожалуйста, введите ваш адрес:")
            await state.set_state(Form.waiting_for_address)
        else:
            main_keyboard = get_main_reply_keyboard()
            await message.answer(f"Приветствую! Я виртуальный ассистент <b>Mr. Kingsman</b>. Чем могу помочь сегодня?", reply_markup=main_keyboard, parse_mode="html")

    @dp.message(F.text == "Купить товар")
    async def buy_item_handler(message: Message):
        user_id = message.from_user.id
        _, _, has_agreed_privacy = get_user_info(user_id)
        if not has_agreed_privacy:
            await message.answer("Пожалуйста, сначала согласитесь на обработку персональных данных, отправив /start.")
            return
        keyboard = get_start_keyboard()
        await message.answer("Что хотите приобрести?", reply_markup=keyboard)

    @dp.message(Form.waiting_for_phone_number)
    async def process_phone_number(message: Message, state: FSMContext):
        user_id = message.from_user.id
        phone_number = message.text

        if phone_number and phone_number.startswith('+7'):
            # Retrieve existing address if any
            address, _, _ = get_user_info(user_id)
            save_user_info(user_id, address, phone_number)
            await message.answer("Спасибо! Ваш номер телефона сохранен.\nПожалуйста, введите ваш адрес:")
            await state.set_state(Form.waiting_for_address)
        else:
            await message.answer("Пожалуйста, введите корректный номер телефона, начинающийся с +7:")
            return # Stay in the same state to re-ask for the phone number

    @dp.message(Form.waiting_for_address)
    async def process_address(message: Message, state: FSMContext):
        user_id = message.from_user.id
        address = message.text

        # Retrieve existing phone number if any
        _, phone_number, _ = get_user_info(user_id)
        save_user_info(user_id, address, phone_number)
        await state.clear()
        main_keyboard = get_main_reply_keyboard()
        await message.answer(f"Спасибо! Ваш адрес \"{address}\" сохранен.\n\nЯ виртуальный ассистент <b>Mr. Kingsman</b>. Чем могу помочь?", reply_markup=main_keyboard, parse_mode="html")

    @dp.message(F.text == "Профиль")
    async def show_profile(message: Message):
        user_id = message.from_user.id
        _, _, has_agreed_privacy = get_user_info(user_id)
        if not has_agreed_privacy:
            await message.answer("Пожалуйста, сначала согласитесь на обработку персональных данных, отправив /start.")
            return

        address, phone_number, _ = get_user_info(user_id)

        profile_message = "<b>Ваш профиль:</b>\n"
        profile_message += f"ID: {user_id}\n"
        profile_message += f"Телефон: {phone_number if phone_number else '-'}\n"
        profile_message += f"Адрес: {address if address else '-'}"

        await message.answer(profile_message, parse_mode="html")

    @dp.message(F.text == "Получить скидку")
    async def get_discount_handler(message: Message):
        user_id = message.from_user.id
        _, _, has_agreed_privacy = get_user_info(user_id)
        if not has_agreed_privacy:
            await message.answer("Пожалуйста, сначала согласитесь на обработку персональных данных, отправив /start.")
            return
        
        # Generate QR code
        qr_data = f"user_id:{user_id}_discount_code:{hash(user_id)}"
        qr_img = qrcode.make(qr_data)
        
        # Save QR code to a temporary file
        qr_filename = f"qr_code_{user_id}.png"
        qr_img.save(qr_filename)
        
        # Send QR code to user
        from aiogram.types import FSInputFile
        photo = FSInputFile(qr_filename)
        await message.answer_photo(photo, caption="Ваш персональный QR-код на скидку!")

    @dp.callback_query(F.data == "agree_privacy", Form.waiting_for_consent)
    async def process_agree_privacy(callback: CallbackQuery, state: FSMContext):
        user_id = callback.from_user.id
        update_user_consent(user_id, True)
        await callback.message.edit_text("Спасибо за ваше согласие!", parse_mode="html")

        # Now proceed with the initial flow (ask for phone number or show main menu)
        address, phone_number, _ = get_user_info(user_id)
        if not phone_number:
            await callback.message.answer("Пожалуйста, введите ваш номер телефона (начиная с +7):")
            await state.set_state(Form.waiting_for_phone_number)
        elif not address:
            await callback.message.answer("Пожалуйста, введите ваш адрес:")
            await state.set_state(Form.waiting_for_address)
        else:
            main_keyboard = get_main_reply_keyboard()
            await callback.message.answer(f"Приветствую! Я виртуальный ассистент <b>Mr. Kingsman</b>. Чем могу помочь сегодня?", reply_markup=main_keyboard, parse_mode="html")
        await callback.answer()

    @dp.callback_query(F.data == "disagree_privacy", Form.waiting_for_consent)
    async def process_disagree_privacy(callback: CallbackQuery, state: FSMContext):
        await callback.message.edit_text("К сожалению, без вашего согласия на обработку персональных данных вы не сможете пользоваться ботом.", parse_mode="html")
        await state.clear()
        await callback.answer()

    # Gate all other callback handlers as well
    @dp.callback_query(~StateFilter(Form.waiting_for_consent))
    async def gated_callback_handler(callback: CallbackQuery):
        user_id = callback.from_user.id
        _, _, has_agreed_privacy = get_user_info(user_id)
        if not has_agreed_privacy:
            privacy_text = (
                "Пожалуйста, сначала согласитесь на обработку персональных данных, "
                "отправив /start и выбрав 'Согласен'."
            )
            await callback.message.answer(privacy_text, parse_mode="html")
            await callback.answer()
            return

    await register_callback_handlers(dp)

    # Start the push notification background task
    asyncio.create_task(send_push_notifications(bot))

    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())