from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from models import Tour, Destination  
from qyerysets import *  

kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Выбрать тур')],
    [KeyboardButton(text='Поиск туров по странам')],
    [KeyboardButton(text='Поиск туров по названию')],
    [KeyboardButton(text='Мои бронирования')],
  ], resize_keyboard=True, input_field_placeholder='Выберите кнопку')


PAGE_SIZE = 2
async def get_tours_kb(page):
    offset = (page - 1) * PAGE_SIZE
    kb = InlineKeyboardBuilder()
    tours = await all_tour(offset=offset,limit=PAGE_SIZE)
    for tour in tours:
        kb.add(InlineKeyboardButton(text=tour.title, callback_data=f'tour_{tour.id}'))

    if page > 1:
        kb.add(InlineKeyboardButton(text="◀️", callback_data=f'page_{page-1}'))

    if len(tours) == PAGE_SIZE:
        kb.add(InlineKeyboardButton(text="▶️", callback_data=f'page_{page+1}'))
    return kb.adjust(2).as_markup()

PAGE_SIZE = 2
async def get_destination_kb(page):
    offset = (page - 1) * PAGE_SIZE
    kb = InlineKeyboardBuilder()
    destinations = await all_destination(offset=offset,limit=PAGE_SIZE)
    for destination in destinations:
        kb.add(InlineKeyboardButton(text=destination.country, callback_data=f'destination_{destination.id}'))

    if page > 1:
        kb.add(InlineKeyboardButton(text="◀️", callback_data=f'page_{page-1}'))

    if len(destinations) == PAGE_SIZE:
        kb.add(InlineKeyboardButton(text="▶️", callback_data=f'page_{page+1}'))
    return kb.adjust(2).as_markup()



async def get_tour_by_destination_kb(destinations_id):
    kb = InlineKeyboardBuilder()
    tours = await get_tour_by_destination(destinations_id)
    for tour in tours:
        kb.add(InlineKeyboardButton(text=tour.title,
            callback_data=f"tour_{tour.id}"))
    kb.add(InlineKeyboardButton(text='Назад', callback_data=f'back_to_dest'))
    return kb.adjust(2).as_markup()

async def back_kb():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Назад', callback_data=f'back_to_dest'))
    return kb.adjust(2).as_markup()




PAGE_SIZE = 2 

async def get_book_kb(page):
    offset = (page - 1) * PAGE_SIZE
    kb = InlineKeyboardBuilder()
 
    async with async_session() as session:
        result = await session.execute(select(Booking).offset(offset).limit(PAGE_SIZE))
        books = result.scalars().all()

    for book in books:
        kb.add(InlineKeyboardButton(text=book.tour_id, callback_data=f'book_{book.id}'))

    if page > 1:
        kb.add(InlineKeyboardButton(text="◀️", callback_data=f'page_{page-1}'))

    if len(books) == PAGE_SIZE:
        kb.add(InlineKeyboardButton(text="▶️", callback_data=f'page_{page+1}'))
    
    return kb.adjust(2).as_markup()


async def get_tour_kb_admin():
    kb = InlineKeyboardBuilder()
    tours = await all_tours()
    for tour in tours:
        kb.add(InlineKeyboardButton(text=tour.title, callback_data=f'movie2_admin_{tour.id}'))
    return kb.adjust(2).as_markup()


