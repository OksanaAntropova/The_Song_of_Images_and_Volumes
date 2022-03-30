from datetime import date

from loggers import liege_logger
from methods import delete_hero, print_db, add_hero, add_motto, add_story, add_combat
from tables import Base, engine


def create_db():
    """
    Drop all the data and create all the tables from scratch
    """
    Base.metadata.drop_all(engine)
    liege_logger.warning("Oh no! The Night King erased the history of this world!")
    Base.metadata.create_all(engine)


def seed_db_with_test_data():
    """
    Seed the database with the following test data
    """

    tyrion_story = """The youngest child of Lord Tywin Lannister. As Tyrion 
is born a dwarf and his mother died during childbirth, he is resented by Tywin 
since birth. Tyrion uses his status as a Lannister partly to mitigate the prejudice 
he has received all of his life, especially from Tywin and his sister, Cersei 
Lannister. He soothes his inadequacies with wine, wit and self-indulgence"""

    # Ещё немного хулиганства или дань местному языку)))
    jaime_story = """Sör Jaime Lannister, Lord Tywin Lannister'ın büyük oğlu,  
Kraliçe Cersei Lannister'ın ikiz kardeşi ve Tyrion Lannister'ın ağabeyiydi. 
Cersei ile ensest bir ilişkiye dahil oldu ve çoğu kişi tarafından bilinmeyen, 
üç çocuğunun, Joffrey, Myrcella Tommen ve doğmamış çocuğunun biyolojik babasıydı."""

    the_hound_story = """Sandor Clegane, popularly known as the Hound, is a skilled warrior 
and the personal bodyguard of Prince Joffrey Baratheon. He is known primarily for 
the horrible facial scarring he bears on the right side of his face and for his 
fierce demeanor and lack of chivalry. Sandor is the younger brother of Ser Gregor 
Clegane, nicknamed "the Mountain", a monstrously huge knight and arguably the most 
feared man in Westeros."""

    arya_story = """Arya Stark is the youngest daughter and third child of Lady Catelyn 
and Lord Ned Stark. Arya was born and raised at Winterfell. She has an older sister, 
Sansa, an older brother Robb, two younger brothers Bran and Rickon Stark, and a 
"bastard half-brother" Jon Snow. Arya rejects the notion that she must become a lady 
and marry for influence and power. Instead, she believes that she can forge her own 
destiny. She is fascinated by warfare and training in the use of arms, and is bored 
by embroidery and other "lady-like" pursuits. She takes after her father and has a 
quarrelsome relationship with her sister Sansa, due to their contrasting interests 
and personalities. She is close to her "half-brother" Jon, who is also something 
of an outsider."""

    bran_story = """Bran is the fourth child and second son of Lady Catelyn and 
Lord Ned Stark. He was born and raised at Winterfell. Bran was named for Ned's elder 
brother, Brandon, who was brutally executed by the Mad King along with Bran's paternal 
grandfather Rickard Stark. He is only called "Brandon" by his mother when he has done 
something wrong. Bran dreams of being a knight of the Kingsguard, and his favorite hobby 
is climbing the walls of Winterfell, using its old rooftops and passageways to get around."""

    hodor_story = """Hodor, originally named Wylis, is a simpleminded servant of House Stark 
at Winterfell working in the stables. He is only capable of saying one word, "hodor", 
though he can apparently understand complex instructions other people give him. "Hodor" 
is a seemingly nonsense word, though in the process it became the name everyone calls him.
Hodor is incredibly large and strong. While he is slow of wits, he is gentle and loyal to 
the Starks. He is actually Old Nan's great-grandson and only known relative."""

    add_hero(name="Tyrion", side="Lannisters", birthday=date(264, 2, 29))
    add_hero(name="Jaime", side="Lannisters")
    add_hero(name="The Hound", side="Lannisters")
    add_hero(name="Arya", side="Starks")
    add_hero(name="Bran", side="Starks")
    add_hero(name="Hodor", side="Starks")
    add_motto(motto="Hear me roar", hero_id=1)
    add_motto(motto="Lannisters always pay their debts", hero_id=1)
    add_motto(motto="The things we do for love", hero_id=2)
    add_motto(motto="Sing for me, bird", hero_id=3)
    add_motto(motto="Stick Them With The Pointy End", hero_id=4)
    add_motto(motto="A girl has no name", hero_id=4)
    add_motto(motto="A girl is Arya Stark of Winterfell, and I'm going home", hero_id=4)
    add_motto(motto="Fly!", hero_id=5)
    add_motto(motto="I'm the memory of this world", hero_id=5)
    add_motto(motto="Hodor!", hero_id=6)
    add_motto(motto="Hodor!Hodor!Hodor!Hodor!Hodor!", hero_id=6)
    add_motto(motto="HOLD THE DOOR!", hero_id=6)  # Ooops, a tiny spoiler sneaked in
    add_story(story=tyrion_story, hero_id=1)
    add_story(story=jaime_story, hero_id=2)
    add_story(story=the_hound_story, hero_id=3)
    add_story(story=arya_story, hero_id=4)
    add_story(story=bran_story, hero_id=5)
    add_story(story=hodor_story, hero_id=6)

    for i in range(5):
        add_combat()


def demonstration():
    create_db()
    seed_db_with_test_data()
    print_db()
    delete_hero("Tyrion")
    print_db()


if __name__ == '__main__':
    demonstration()
