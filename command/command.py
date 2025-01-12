from aiogram import Router, types
from aiogram.filters import Command,CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
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
    await message.answer(f'Мои бронирования', reply_markup=await get_book_kb(page=1))


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


    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Бронировать", callback_data=f"add_dish_{tour_id}")]])
    await callback.message.answer("Бронировать?\nДля просмотра бронированные нажмите на кнопку Мои бронирование", reply_markup=keyboard)
  


@command_router.callback_query(F.data.startswith("add_tour"))
async def add_tour_to_cart(callback: CallbackQuery):
    tour_id = callback.data.split("_")[2]
    tour = await get_tour_by_id(tour_id)
    user_id = callback.from_user.id
    User[user_id].append(tour)
    await callback.answer(f"'{tour.title}' забронирвано!", show_alert=True)



    
 

@command_router.callback_query(F.data == "book_")
async def checkout_handler(callback: CallbackQuery, state):
    user_id = callback.from_user.id
    cart = User[user_id]
    if not cart:
        await callback.message.answer("Пусто.")
        return

    await state.update_data(cart=cart)
    await callback.message.answer("Оставьте свои данные мы связимся с вами в ближайщее время:")
  


   





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


@command_router.callback_query(F.data.startswith('page_'))
async def page_hadler(callback: CallbackQuery):
    data = callback.data.split('_')[1]
    id  = int(data)
    await callback.message.edit_reply_markup(reply_markup=await get_book_kb(page=id))



    # booking = session.query(Booking).filter_by(user_id=user_id).all()

    # if not booking:
    #     await message.answer("У вас нет забронированных туров")
    # else:
    #     response = "Ваши бронирования:\n"
    #     for book in booking:
    #         response += f"-{book.tour_id}\n"
    #         await message.answer(response)




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




    












