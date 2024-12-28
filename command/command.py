from aiogram import Router, types
from aiogram.filters import Command,CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile, URLInputFile
from aiogram import F
import re
from command.keyboards import *
from aiogram.utils.media_group import MediaGroupBuilder
from sqlalchemy.orm import Session
from models import Booking


command_router = Router()


@command_router.message(Command('start'))
async def message_handler(message:Message):
    await message.answer('Привет! Я бот подборке разных туров', reply_markup=kb)


@command_router.message(F.text == 'Выбрать тур')
async def tours_handler(message: Message):
    await message.answer(f'Выбрать тур', reply_markup=await get_tours_kb(page=1))

@command_router.message(F.text == 'Выбрать туров по странам')
async def tours_handler(message: Message):
    await message.answer(f'Выбрать туров по странам', reply_markup=await get_destination_kb(page=1))


@command_router.message(F.text == 'Мои бронирования')
async def movies_handler(message: Message):
    await message.answer(f'Мои бронирования', reply_markup=await get_book_kb())


@command_router.callback_query(F.data.startswith('tour_'))
async def tour_detail_handler(callback: CallbackQuery):
    tour_id = callback.data.split('_')[1]  
    tour = await get_tour_by_id(tour_id=tour_id)
    album = MediaGroupBuilder(caption=f'Название: {tour.title}\n'
                                                f'Возрастное огранечение: {tour.age_limit}\n'
                                                f'Описание: {tour.description}\n'
                                                f'Цена: {tour.price}\n'
                                                f'Длительность: {tour.duration}\n'
                                                f'Начало тура: {tour.start_date}\n'
                                                f'Конец тура: {tour.end_date}\n'
                                         )
    
    if tour.image.startswith('http') or tour.image.startswith('AgA'):
        album.add_photo(media=tour.image)
       
    else:
         album.add_photo(media=FSInputFile(tour.image))  

    await callback.message.answer_media_group(media=album.build()) 

  


@command_router.callback_query(F.data.startswith('page_'))
async def page_hadler(callback: CallbackQuery):
    data = callback.data.split('_')[1]
    id  = int(data)
    await callback.message.edit_reply_markup(reply_markup=await get_tours_kb(page=id))



@command_router.callback_query(F.data.startswith('destination_'))
async def tour_by_distination_handler(callback: CallbackQuery):
    await callback.message.delete()
    d_id = callback.data.split('_')[1]  
    await callback.message.answer(f'Туры по этой стране',
        reply_markup=await get_tour_by_destination_kb(d_id))
    

@command_router.callback_query(F.data.startswith('back_to_dest'))
async def back_to_destination_handler(callback:CallbackQuery):
    await callback.message.answer('Выберите страну', reply_markup=await get_destination_kb(page=1))


@command_router.callback_query(F.data.startswith('page_'))
async def page_hadler(callback: CallbackQuery):
    data = callback.data.split('_')[1]
    id  = int(data)
    await callback.message.edit_reply_markup(reply_markup=await get_destination_kb(page=id))



@command_router.message(F.text == 'Мои бронирование')
async def my_booking(message:types.Message):
    session: Session = Session()


    booking = session.query(Booking).filter_by(user_id=user_id).all()

    if not booking:
        await message.answer("У вас нет забронированных туров")
    else:
        response = "Ваши бронирования:\n"
        for book in booking:
            response += f"-{book.tour_id}\n"
            await message.answer(response)




from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class FindTour(StatesGroup):
    title = State()

@command_router.message(F.text == 'Поиск туров по названию')
async def find_tour_handler(message: Message, state: FSMContext):
    await message.answer('Введите название тура')
    await state.set_state( FindTour.title)

@command_router.message( FindTour.title)
async def find_tour_handler(message: Message, state: FSMContext):
    search_title = message.text.strip()
    if search_title:
        tours = await get_tour_title(search_title)
        if tours:
            kb=InlineKeyboardBuilder()
            for t in tours:
                kb.add(InlineKeyboardButton(text=t.title, callback_data=f'tour_{t.id}'))
                await message.answer(f' Туры по вашему запросу:',reply_markup=kb.adjust(2).as_markup())

        else:
            await message.answer('Туры не найдены')

    else:
        await message.answer('Введите название туров')
    await state.clear()




    












