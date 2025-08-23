import asyncio
import logging

from aiogram import Bot, Dispatcher, html
from aiogram.filters import CommandStart
from aiogram.types import Message

# Configure logging
logging.basicConfig(level=logging.INFO)

# Replace with your actual bot token
BOT_TOKEN = "7559529190:AAHQE5Wim83zkzgV79SY9FvP8lU_r0ftM34"

# Main functiond
async def main() -> None:
    # Initialize Bot and Dispatcher
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    
    # All handlers should be async
    @dp.message(CommandStart())
    async def command_start_handler(message: Message) -> None:
        """
        This handler receives messages with `/start` command
        """
        await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

    # Register handlers (if you had more, you'd register them here)
    # dp.include_router(router) # Only if using a separate router

    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())