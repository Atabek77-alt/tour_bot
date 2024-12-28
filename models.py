from sqlalchemy import String, Integer, Column, ForeignKey, Date, Float, Text, Table, Boolean
from sqlalchemy.orm import relationship, sessionmaker, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    pass







destinations_tour = Table("tour_destinations", Base.metadata,
    Column("destinations_id", Integer, ForeignKey("destinations.id"), primary_key=True),
    Column("tour_id", Integer, ForeignKey("tours.id"), primary_key=True))

class User(Base):
    __tablename__ = "user"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id:Mapped = mapped_column(Integer, nullable=False)



class Tour(Base):
    __tablename__ = "tours"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    image:Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    age_limit:Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    duration:Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[Date] = mapped_column(Date)
    end_date: Mapped[Date] = mapped_column(Date)
    
  

 
    destinations = relationship("Destination", secondary=destinations_tour, back_populates="tours")



class Destination(Base):
    __tablename__ = 'destinations'

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(150))
    country:Mapped[str] = mapped_column(String(100), nullable=False)
    description:Mapped[str] = mapped_column(Text)
    best_season:Mapped[str] = mapped_column(String(199))
    visa:Mapped[bool] = mapped_column(Boolean) 
    image:Mapped[str] = mapped_column(String(255))

    tours = relationship("Tour", secondary=destinations_tour, back_populates="destinations")

    







class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tour_id: Mapped[int] = mapped_column(Integer, ForeignKey("tours.id"))
    hotel_id: Mapped[int] = mapped_column(Integer, ForeignKey("hotels.id"))
    excursion_id: Mapped[int] = mapped_column(Integer, ForeignKey("excursions.id"))
    booking_date: Mapped[Date] = mapped_column(Date)
    total_price: Mapped[Float] = mapped_column(Float)

  
    tour = relationship("Tour", backref="bookings")



from config import MYSQL_URL
engine = create_async_engine(MYSQL_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=True)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)