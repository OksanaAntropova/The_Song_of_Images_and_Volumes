from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.event import listen
from sqlalchemy.sql.functions import func
from sqlalchemy import UniqueConstraint
from random import randrange
from datetime import date
import logging

logging.basicConfig(
    filename="A_Song_of_Ice_and_Fire.txt",
    format="%(asctime)s => %(message)s",
 #   datefmt="%Y-%m-%d %I:%M:%S.%f", # I -12H time, H - 24 hour time
    level=logging.DEBUG
)

Base = declarative_base()


class Mottoes(Base):
    """
    Слоганы героев: id, hero_id, motto_id (нумерация у каждого героя с 1),
    motto (текст слогана). У каждого героя должно быть от 1-го до нескольких слоганов.
    """
    __tablename__ = "mottoes"
    # __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    motto = Column(String())
    motto_id = Column(Integer)
    hero_id = Column(Integer, ForeignKey("heroes.id"))
    hero = relationship("Heroes", back_populates="mottoes")

    __table_args__ = (UniqueConstraint(hero_id, motto_id),)

    # Честно потырила вот отсюда https://stackoverflow.com/questions/34352584/sqlalchemy-how-to-auto-increment-based-on-multiple-keys
    @staticmethod
    def increment(mapper, connection, mottoes):
        last = Session().query(func.max(Mottoes.motto_id).label('last')) \
            .filter(Mottoes.hero_id == mottoes.hero_id).first()
        mottoes.motto_id = last.last + 1 if last.last else 1

    def __repr__(self):
        return f"my id {self.id}, hero id {self.hero_id}, motto id {self.motto_id}, hero: {self.hero}, motto: {self.motto}"

    logging.info("The table of Mottoes is successfully created")


listen(Mottoes, "before_insert", Mottoes.increment)


class Combats(Base):
    """
    Столкновения героев: id, hero_1_id, hero_1_moto_id (= id таблицы слоганов),
    hero_2_id, hero_2_moto_id, winner (0 для ничьей, 1 для героя 1, 2 для героя 2).
    Герой 1 - тот, кто инициировал столкновение или напал первый или нанёс первый удар.
    Если невозможно определить - то случайный герой.
    """
    __tablename__ = "combats"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    hero_1_id = Column(Integer, ForeignKey('heroes.id'))
    hero_1_motto_id = column_property(
        select(Mottoes.id).
            where(Mottoes.hero_id == hero_1_id).limit(1).
            scalar_subquery()
    )
    hero_2_id = Column(Integer, ForeignKey('heroes.id'))
    hero_2_motto_id = column_property(
        select(Mottoes.id).
            where(Mottoes.hero_id == hero_2_id).limit(1).
            scalar_subquery()
    )
    winner = Column(Integer)  # , default=randrange(3) Почему всё время одно число?

    def __repr__(self):
        return f"{self.hero_1_id}, {self.hero_1_motto_id} vs. {self.hero_2_id}, {self.hero_2_motto_id}: winner = {self.winner}"

    logging.info("The table of Combats is successfully created")


class Heroes(Base):  # Класс должен называться множественным числом? Или единственным?
    """
    Герои: id, side (сторона, принадлежность), name, birthday, + любые (!!!) House?
    на ваше усмотрение. Минимум 3 героя на каждой стороне.
    НЕОБЯЗАТЕЛЬНО: числовая сила героя, которая влияет на вероятность победы.
    """
    __tablename__ = "heroes"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    birthday = Column(Date)
    side = Column(String(30))
    # one-to-many collection
    mottoes = relationship("Mottoes", back_populates="hero")  # , cascade="all, delete"Разобраться с order_by
    # one-to-one Heroes.story
    story = relationship("Stories", back_populates="hero", uselist=False)  # , cascade="all, delete"
    combatants = relationship("Heroes", secondary="combats",
                              primaryjoin=id == Combats.hero_1_id,
                              secondaryjoin=id == Combats.hero_2_id,
                              )

    #     heroes_attacked = relationship(
    #         "Heroes",
    #         secondary=combats,
    #         primaryjoin=id==Combats.hero_1_id,
    #                            secondaryjoin=id==Combats.hero_2_id,
    #         back_populates="was_attacked_by_heroes")
    #     was_attacked_by_heroes = relationship(
    #         "Heroes",
    #         secondary=Combats,
    #         back_populates="heroes_attacked")
    #     heroes_attacked = relationship(
    #         "Heroes",
    #         secondary=Combats,
    #         back_populates="was_attacked_by_heroes")
    #     was_attacked_by_heroes = relationship(
    #         "Heroes",
    #         secondary=Combats,
    #         back_populates="heroes_attacked")

    def __repr__(self):
        return f"{self.id}: {self.name} / House of {self.side} / {self.birthday}"

    logging.info("The table of Heroes is successfully created")


class Stories(Base):
    """
    Краткая предыстория героя без спойлеров: id, hero_id, story. Где 1 герой = строго 1 история.
    """
    __tablename__ = 'stories'
    id = Column(Integer, primary_key=True)
    story = Column(String())
    hero_id = Column(Integer, ForeignKey('heroes.id'))
    hero = relationship("Heroes", back_populates="story")

    def __repr__(self):
        return f"my id {self.id}, hero id {self.hero_id}, hero: {self.hero}, story: {self.story}"

    logging.info("The table of Stories is successfully created")