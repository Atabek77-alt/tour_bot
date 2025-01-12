from models import *
from sqlalchemy import select, update, delete
from datetime import date




async def add_tour(tour):
    async with async_session() as session:
       
        # tour = Tour(
        #     title="Тур в Дубай",
        #     image='images/dubai.png',
        #     description='great city',
        #     age_limit=18,
        #     price=2000,
        #     duration=7,  
        #     start_date=date(2025, 1, 1),
        #     end_date=date(2025, 1, 20)
        # )
        # tour1 = Tour(
        #     title="Тур на Бали",
        #     image='images/dubai.png',
        #     description='хорошо подойдет для семейного отдыха',
        #     age_limit=18,
        #     price=3000,
        #     duration=14,  
        #     start_date=date(2025, 3, 2),
        #     end_date=date(2025, 3, 27)
        
        session.add(tour)
       
        await session.commit()


async def add_destination(dest):
    async with async_session() as session:
        # dest = Destination(
        #     name='Dubai',
        #     country='UAE',
        #     description='very good country for relax',
        #     best_season='winter',
        #     visa=True,
        #     image='images/UAE.png'
        # )
        # dest1 = Destination(
        #     name='Thailand',
        #     country='Thailand',
        #     description='very good country for family relax',
        #     best_season='winter',
        #     visa=True,
        #     image='images/UAE.png'
    # )
        session.add(dest)
        # session.add(dest1)
        await session.commit() 



async def add_book(book):
    async with async_session() as session:
        # book = Booking(
           
        #     tour_id=1,
           
        #     booking_date=date(2024, 12, 30),
        #     total_price=2380
        # )
        # book1 = Booking(
          
        #     tour_id=1,
            
        #     booking_date=date(2025, 1, 1),
        #     total_price=850
        # )
        session.add(book)
        # session.add(book1)
        await session.commit()





async def get_tour_by_id(tour_id):
    async with async_session() as session:
        result = await session.scalar(select(Tour).where(Tour.id==tour_id))
        return result 


async def get_destination_by_id(destination_id):
    async with async_session() as session:
        result = await session.scalar(select(Destination).where(Destination.id==destination_id))
        return result


async def all_tour(limit,offset):
    async with async_session() as s:
        result = await s.scalars(select(Tour).offset(offset).limit(limit))
        return result.all()


async def all_tours():
    async with async_session() as s:
        result = await s.scalars(select(Tour))
        return result.all()



async def get_tour_title(tit):
    async with async_session() as s:
        result = await s.scalars(select(Tour).where(Tour.title.ilike(f'%{tit}%')))
        return result.all()


async def all_destination(limit,offset):
    async with async_session() as s:
        result = await s.scalars(select(Destination).offset(offset).limit(limit))
        return result.all()
    


async def all_books(limit,offset):
     async with async_session() as s:
        result = await s.scalars(select(Booking).offset(offset).limit(limit))
        return result.all()


async def add_tour_destination(t, d):
    async with async_session() as session:
        trm = destinations_tour.insert().values(tour_id=t, destinations_id=d)
        await session.execute(trm)
        await session.commit()


async def get_tour_by_destination(destination_id):
    async with async_session() as session:
        result = await session.scalars(
            select(Tour).join(destinations_tour).where(destinations_tour.c.destination_id == destination_id)
        )
        return result







