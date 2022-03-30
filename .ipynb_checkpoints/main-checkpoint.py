from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from src.tables import Base, Heroes, Mottoes, Stories, Combats
from src.methods import add_motto, add_hero, add_story, add_combat, delete_hero


def print_db():
    line = '=' * 10
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


engine = create_engine('postgresql://postgres:pwd0123456789@localhost:5432/my_database')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


Tyrion_story = """The youngest child of Lord Tywin Lannister. As Tyrion is born a dwarf and his mother died 
during childbirth, he is resented by Tywin since birth. Tyrion uses his status as a Lannister partly to 
mitigate the prejudice he has received all of his life, especially from Tywin and his sister, Cersei Lannister. 
He soothes his inadequacies with wine, wit and self-indulgence"""

add_hero(name="Tyrion", side="Lannisters", birthday=date(264, 2, 29))
add_hero(name="Jaime", side="Lannisters")
add_hero(name="Cersei", side="Lannisters")
add_hero(name="Arya", side="Starks")
add_hero(name="Bran", side="Starks")
add_motto(motto="Hear me roar", hero_id=1)
add_motto(motto="Lannisters always pay their debts", hero_id=1)
add_motto(motto="The things we do for love", hero_id=2)
add_motto(motto="Lannisters always pay their debts", hero_id=3)
add_motto(motto="Stick Them With The Pointy End", hero_id=4)
add_motto(motto="Fly!", hero_id=5)
add_motto(motto="I'm the memory of this world", hero_id=5)
add_story(story=Tyrion_story, hero_id=1)

for i in range(5):
    add_combat()

print_db()

delete_hero("Tyrion")

print_db()
