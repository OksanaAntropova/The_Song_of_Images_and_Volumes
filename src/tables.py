import os
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.functions import func

from loggers import liege_logger

DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")
# DB_CONNECTION_STRING = 'postgresql://georgerrmartin:thelastbookiscoming@localhost:5432/game_of_thrones'
# DB_CONNECTION_STRING = 'postgresql://georgerrmartin:thelastbookiscoming@localhost:5432/game_of_thrones_prod'

engine = create_engine(DB_CONNECTION_STRING)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Mottoes(Base):
    """
    The table of Mottoes:
        - id, # end-to-end numbering for all the heroes
        - hero_id,
        - motto_id, # separate numbering for each hero [hero1: motto1, motto2, ...;
                                                        hero2: motto1, ...]
        - motto.
    """
    __tablename__ = "mottoes"

    id = Column(Integer, primary_key=True)
    motto = Column(String())
    motto_id = Column(Integer)
    hero_id = Column(Integer, ForeignKey("heroes.id"))
    hero = relationship("Heroes", back_populates="mottoes")

    __table_args__ = (UniqueConstraint(hero_id, motto_id),)

    # Честно потырила вот отсюда
    # https://stackoverflow.com/questions/34352584/sqlalchemy-how-to-auto-increment-based-on-multiple-keys
    @staticmethod
    def increment(mapper, connection, mottoes):
        last = Session().query(func.max(Mottoes.motto_id).label('last')) \
            .filter(Mottoes.hero_id == mottoes.hero_id).first()
        mottoes.motto_id = last.last + 1 if last.last else 1

    def __repr__(self):
        return f"{self.id}, hero id: {self.hero_id}, motto id: {self.motto_id}, {self.motto}"

    liege_logger.info("The table of Mottoes is successfully created")


listen(Mottoes, "before_insert", Mottoes.increment)


class Combats(Base):
    """
    The table of Combats:
        - id,
        - hero_1_id,
        - hero_1_motto_id, [= Mottoes.motto_id],
        - hero_2_id,
        - hero_2_motto_id, [= Mottoes.motto_id]
        - winner. # 0 - a tie, 1 - hero1 won, 2 - hero2 won
    """
    __tablename__ = "combats"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    hero_1_id = Column(Integer, nullable=False)
    hero1 = relationship("Heroes", foreign_keys=hero_1_id, primaryjoin="Combats.hero_1_id==Heroes.id")
    hero_1_motto_id = Column(Integer, nullable=False)
    # hero_1_motto_id = column_property( # Так автоматом прикручивается первый, а надо случайный(
    #     select(Mottoes.id).            # Не успела разобраться как автоматом сделать тут random, поэтому костыль(
    #         where(Mottoes.hero_id == hero_1_id).limit(1).
    #         scalar_subquery()
    # )
    hero_2_id = Column(Integer, nullable=False)
    hero2 = relationship("Heroes", foreign_keys=hero_2_id, primaryjoin="Combats.hero_2_id==Heroes.id")
    hero_2_motto_id = Column(Integer, nullable=False)
    # hero_2_motto_id = column_property(
    #     select(Mottoes.id).
    #         where(Mottoes.hero_id == hero_2_id).limit(1).
    #         scalar_subquery()
    # )
    winner = Column(Integer)  # , default=randrange(3) Почему всё время одно число?

    def __repr__(self):
        return f"{self.id}#{self.hero_1_id}, {self.hero_1_motto_id} vs. {self.hero_2_id}, {self.hero_2_motto_id}: winner = {self.winner}"

    liege_logger.info("The table of Combats is successfully created")


class Heroes(Base):
    """
    The table of Heroes:
        - id,
        - name,
        - house, # Пока не реализовано!
        - side. [Lannisters or Starks] # I'm so sorry for this simplification, dear George RR!
    """
    __tablename__ = "heroes"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    birthday = Column(Date)
    side = Column(String(30))
    mottoes = relationship("Mottoes", back_populates="hero", cascade="all, delete")
    story = relationship("Stories", back_populates="hero", uselist=False, cascade="all, delete")

    def __repr__(self):
        return f"{self.id}: {self.name} / House of {self.side} / {self.birthday}"

    liege_logger.info("The table of Heroes is successfully created")


class Stories(Base):
    """
    The table of Stories:
        - id,
        - hero_id,
        - story. # Don't worry! No spoilers.
    """
    __tablename__ = 'stories'
    id = Column(Integer, primary_key=True)
    story = Column(String())
    hero_id = Column(Integer, ForeignKey('heroes.id'))
    hero = relationship("Heroes", back_populates="story")

    def __repr__(self):
        return f"{self.id}, hero id: {self.hero_id}\n{self.story}"

    liege_logger.info("The table of Stories is successfully created")
