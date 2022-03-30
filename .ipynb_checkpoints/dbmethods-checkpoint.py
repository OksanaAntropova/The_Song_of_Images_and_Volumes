from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.tables import Heroes, Mottoes, Stories, Combats

engine = create_engine('postgresql+psycopg2://postgres_user:rootroot@localhost:5000/horizons_world')
Session = sessionmaker(bind=engine)


def add_hero(name: str, side: str, birthday: date = date(200, 1, 1)) -> None:
    """
    Adds a new hero to the Heroes table
    """
    with Session() as session:  # Подумать насчёт даты
        session.add(Heroes(name=name, side=side, birthday=birthday))
        session.commit()
    logging.info(f"{name} was successfully added to the Heroes table")


def add_motto(motto: str, hero_id: int) -> None:
    """
    Adds a new motto to the Mottoes table
    """
    # добавление слогана героя (если такого героя нет - падать с ошибкой).
    # И так падает с ошибкой ForeignKeyViolation
    with Session() as session:
        session.add(Mottoes(motto=motto, hero_id=hero_id))
        session.commit()
    logging.info(f"The hero with id {hero_id} now can shout '{motto}'")


def add_story(story: str, hero_id: int) -> None:
    """
    Adds a new story to the Stories table
    """
    with Session() as session:
        session.add(Stories(story=story, hero_id=hero_id))
        session.commit()
    logging.info(f"The history of hero with id {hero_id} is:\n{story}")


def add_combat() -> None:
    """
    Adds a new combat to the Combats table
    """
    """
    добавление столкновения (случайно выбираются герои РАЗНЫХ сторон, случайно выбираются 
    их слоганы, случайный победитель).
    https://stackoverflow.com/questions/60805/getting-random-row-through-sqlalchemy
    """

    def get_random_hero_id_of_side(side):
        """
        Returns the id of a random hero from the given side
        """
        list_of_heroes_id = Session().query(Heroes.id).where(Heroes.side == side).all()
        return list_of_heroes_id[randrange(len(list_of_heroes_id))][0]

    hero_1_id = get_random_hero_id_of_side("Lannisters")
    hero_2_id = get_random_hero_id_of_side("Starks")
    winner = randrange(3)
    with Session() as session:
        session.add(Combats(hero_1_id=hero_1_id,
                            hero_2_id=hero_2_id,
                            winner=winner))
        session.commit()
    logging.info(f"The hero with id {hero_1_id} attacked the hero with id {hero_2_id}. Result: {winner}")


def delete_hero(name: str) -> None:
    """
    Delete a hero from the Heroes, Mottoes and Stories tables.
    The hero will stay in the Combats table
    """
    with Session() as session:
        # session.execute(delete(Heroes).where(Heroes.name == "Tyrion"))
        hero = session.query(Heroes).where(Heroes.name == name).first()
        session.delete(hero)
        session.commit()
    logging.info(f"{name} was successfully deleted from the Heroes, Mottoes and Stories tables")