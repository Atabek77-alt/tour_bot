import asyncio
from aiogram import Bot, Dispatcher
from models import *
import sys, logging 
from config import TOKEN
from command.command import command_router
from models import create_tables
from qyerysets import *
from admin import admin_router







# async def main():
   
    # await add_tour_destination()
#     await add_tour()
#     await add_destination()
#     await add_hotel()
#     await add_excurs()
#     await add_book()




async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(command_router, admin_router)
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())  

















