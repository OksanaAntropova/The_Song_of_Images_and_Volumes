from datetime import date
from random import randrange

from loggers import liege_logger, combat_logger
from tables import Session
from tables import Heroes, Mottoes, Stories, Combats


def add_hero(name: str, side: str, birthday: date = date(200, 1, 1)) -> None:
    """
    Add a new hero to the Heroes table
    """
    with Session() as session:
        session.add(Heroes(name=name, side=side, birthday=birthday))
        session.commit()
    liege_logger.info(f"{name} was successfully added to the Heroes table")


def add_motto(motto: str, hero_id: int) -> None:
    """
    Add a new motto to the Mottoes table
    """
    # добавление слогана героя (если такого героя нет - падать с ошибкой).
    # И так падает с ошибкой ForeignKeyViolation
    with Session() as session:
        session.add(Mottoes(motto=motto, hero_id=hero_id))
        session.commit()
    liege_logger.info(f"The hero with id {hero_id} now can shout '{motto}'")


def add_story(story: str, hero_id: int) -> None:
    """
    Add a new story to the Stories table
    """
    with Session() as session:
        session.add(Stories(story=story, hero_id=hero_id))
        session.commit()
    liege_logger.info(f"The history of hero with id {hero_id} is:\n{story}")


def add_combat() -> None:
    """
    Add a new combat to the Combats table
    """
    def get_random_hero_id_of_side(side):
        """
        Returns the id of a random hero from the given side
        """
        list_of_heroes_id = Session().query(Heroes.id).where(Heroes.side == side).all()
        return list_of_heroes_id[randrange(len(list_of_heroes_id))][0]

    def get_random_motto_id_of_hero(hero_id):
        """
        Returns the id of a random hero from the given side
        """
        list_of_mottoes_id = Session().query(Mottoes.id).where(Mottoes.hero_id == hero_id).all()
        return list_of_mottoes_id[randrange(len(list_of_mottoes_id))][0]

    hero_1_id = get_random_hero_id_of_side("Lannisters")
    hero_2_id = get_random_hero_id_of_side("Starks")
    hero_1_motto_id = get_random_motto_id_of_hero(hero_1_id)
    hero_2_motto_id = get_random_motto_id_of_hero(hero_2_id)
    winner = randrange(3)

    with Session() as session:
        session.add(Combats(hero_1_id=hero_1_id,
                            hero_2_id=hero_2_id,
                            hero_1_motto_id=hero_1_motto_id,
                            hero_2_motto_id=hero_2_motto_id,
                            winner=winner))
        session.commit()

    combat_logger.info(f"The hero with id {hero_1_id} attacked the hero with id {hero_2_id}. Result: {winner}")


def delete_hero(name: str) -> None:
    """
    Delete a hero from the Heroes, Mottoes and Stories tables.
    The hero will stay in the Combats table
    """
    with Session() as session:
        hero = session.query(Heroes).where(Heroes.name == name).first()
        session.delete(hero)
        session.commit()
    liege_logger.info(f"{name} was successfully deleted from the Heroes, Mottoes and Stories tables")


def print_db(): # Интересно, почему не даёт аннотировать возврат None, когда функция ничего не принимает
    """
    Prints out the current content of the DB
    """
    line = '=' * 20
    print(f"{line}Heroes{line}")
    with Session() as session:
        for hero in session.query(Heroes).all():
            print(hero)
    print(f"{line}Mottoes{line}")
    with Session() as session:
        for motto in session.query(Mottoes).all():
            print(motto)
    print(f"{line}Combats{line}")
    with Session() as session:
        for combat in session.query(Combats).all():
            print(combat)
    print(f"{line}Stories{line}")
    with Session() as session:
        for story in session.query(Stories).all():
            print(story)
    print("\n\n")
