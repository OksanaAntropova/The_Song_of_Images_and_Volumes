import argparse
from datetime import date

from loggers import vassal_logger
from methods import add_motto, add_hero, add_story, add_combat, delete_hero, print_db

description = """Perform one of available actions with the Game of Thrones data base:\n
- add a new hero;\n
- add a new motto for an existing hero;\n
- add a new story for an existing hero;\n
- add a new combat of 2 random heroes from different sides;\n
- delete an existing hero;
- print out all the content of the data base.
"""
parser = argparse.ArgumentParser(description=description)
parser.add_argument("action", type=str, choices=["add_hero",
                                                 "add_motto",
                                                 "add_story",
                                                 "add_combat",
                                                 "delete_hero",
                                                 "print_db"],
                    help="the action you want to perform with the data base")
args = parser.parse_args()

match args.action:
    case "add_hero":
        name = input("Enter the name of a new hero: ")
        side = input("Enter the side the hero fights for. Well... Mostly =D (Lannisters or Starks): ")
        year = int(input("Enter the year of birth of the hero: "))
        month = int(input("Enter the month of birth of the hero: "))
        day = int(input("Enter the day of birth of the hero: "))
        vassal_logger.info(
            f"Adding the hero {name} of {side} side. Born {day}.{month}.{year} after Aegon's Conquest.")
        add_hero(name=name, side=side, birthday=date(year, month, day))
    case "add_motto":
        hero_id = int(input("Enter id of the hero: "))
        motto = input("Enter the motto: ")
        vassal_logger.info(f"Adding a new motto for the hero with id {hero_id}.")
        add_motto(motto=motto, hero_id=hero_id)
    case "add_story":
        hero_id = int(input("Enter id of the hero: "))
        story = input("Enter the hero's story: ")
        vassal_logger.info(f"Adding the story of the hero with id {hero_id}.")
        add_story(story=story, hero_id=hero_id)
    case "add_combat":
        vassal_logger.info(f"Adding a new combat of 2 heroes from opposing sides.")
        add_combat()
    case "delete_hero":
        name = input("Enter the name of the hero to delete: ")
        vassal_logger.info(f"Deleting {name}.")
        delete_hero(name)
    case "print_db":
        print_db()
