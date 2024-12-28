from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardButton
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from command.keyboards import *
from aiogram.utils.media_group import MediaGroupBuilder
from qyerysets import *
from config import ADMIN_ID


admin_router = Router()

class AddTour(StatesGroup):
    add_t_title = State()
    add_t_image = State()
    add_t_description = State()
    add_t_age_limit = State()
    add_t_duration = State()
    add_t_price = State()
    add_t_start_date = State()
    add_t_end_date = State()
    
async def check_admin(message: Message):
    return message.from_user.id == ADMIN_ID


@admin_router.message(Command('add_tour'))
async def add_tour_admin(message: Message, state: FSMContext):
    if not await check_admin(message):
        await message.answer('Это команда только для Администратора')
        return
    await message.answer('Введите название тура')
    await state.set_state(AddTour.add_t_title)


@admin_router.message(AddTour.add_t_title)
async def add_movie_title(message:Message, state: FSMContext):
    await state.update_data(add_t_title=message.text)
    await message.answer('Отправьте фото для обложки тура')
    await state.set_state(AddTour.add_t_image)


@admin_router.message(AddTour.add_t_image)
async def add_movie_title(message:Message, state: FSMContext):
    await state.update_data(add_t_image=message.photo[0].file_id)
    await message.answer('Введите описание для тура')
    await state.set_state(AddTour.add_t_description)



@admin_router.message(AddTour.add_t_description)
async def add_movie_title(message:Message, state: FSMContext):
    await state.update_data(add_t_description=message.text)
    await message.answer('Введите возрастное ограничение тура')
    await state.set_state(AddTour.add_t_age_limit)



@admin_router.message(AddTour.add_t_age_limit)
async def add_movie_title(message:Message, state: FSMContext):
    await state.update_data(add_t_age_limit=message.text)
    await message.answer('Введите длительность тура')
    await state.set_state(AddTour.add_t_duration)




@admin_router.message(AddTour.add_t_duration)
async def add_movie_title(message:Message, state: FSMContext):
    await state.update_data(add_t_duration=message.text)
    await message.answer('Введите стоимость тура')
    await state.set_state(AddTour.add_t_price)



@admin_router.message(AddTour.add_t_price)
async def add_movie_title(message:Message, state: FSMContext):
    await state.update_data(add_t_price=message.text)
    await message.answer('Введите начало числа тура')
    await state.set_state(AddTour.add_t_start_date)


@admin_router.message(AddTour.add_t_start_date)
async def add_movie_title(message:Message, state: FSMContext):
    await state.update_data(add_t_start_date=message.text)
    await message.answer('Введите конец числа тура')
    await state.set_state(AddTour.add_t_end_date)



@admin_router.message(AddTour.add_t_end_date)
async def add_movie_title(message:Message, state: FSMContext):
    await state.update_data(add_t_end_date=message.text)


    data = await state.get_data()
    tour = Tour(
        title = data['add_t_title'],
        image = data['add_t_image'],
        description=data['add_t_description'],
        age_limit=data['add_t_age_limit'],
        price=data['add_t_price'],
        duration=data['add_t_duration'],
        start_date=data['add_t_start_date'],
        end_date=data['add_t_end_date']
    )
    await add_tour(tour)
    await message.answer(f'Название: {data.get('add_t_title')}\n'
                         f'Фото: {data.get('add_t_image')}\n'
                         f'Описание: {data.get('add_t_description')}\n'
                         f'Возрастное ограничение: {data.get('add_t_age_limit')}\n'
                         f'Цена: {data.get('add_t_price')}\n'
                         f'Длительность: {data.get('add_t_duration')}\n'
                         f'Начало тура: {data.get('add_t_start_date')}\n'
                         f'Окончание  тура: {data.get('add_t_end_date')}\n'
                        )
    await state.clear


# class AddDest(StatesGroup):
#     add_d_country=State()
#     add_d_description=State()

# async def check_admin(message: Message):
    # return message.from_user.id == ADMIN_ID


# @admin_router.message(Command('add_dest'))
# async def add_dest_admin(message: Message, state: FSMContext):
#     if not await check_admin(message):
#         await message.answer('Это команда только для Администратора')
#         return
#     await message.answer('Введите название страны')
#     await state.set_state(AddDest.add_d_country)

# @admin_router.message(AddDest.add_d_country)
# async def add_dest_title(message:Message, state: FSMContext):
#     await state.update_data(add_d_country=message.text)
#     await message.answer('Опищите страну')
#     await state.set_state(AddDest.add_d_description)

# @admin_router.message(AddDest.add_d_description)
# async def add_dest_description(message:Message, state: FSMContext):
#     await state.update_data(add_d_description=message.text)

#     data = await state.get_data()
#     dest = Destination(
#         country=data['add_d_country'],
#         description=data['add_d_description']
#     )
#     await add_destination(dest)
#     await message.answer(f'Название страны: {data.get('add_d_country')}\n'
#                          f'Опищите страну: {data.get('add_d_description')}\n'
#                          )
#     await state.clear
    


