from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.db_models import Coffee, Roaster, Method, Brew, Grinder, Roast


def get_session():
    engine = create_engine(
        "postgresql://postgres:postgres@localhost:5432/coffeeculator"
    )
    Session = sessionmaker(engine)
    return Session()


def list_objects(session, db_object):
    ids = []
    for obj in session.query(db_object):
        ids.append(obj.id)
        print(obj)
    return ids


def list_roasters(session):
    print("Roasters we know about:")
    return list_objects(session, Roaster)


def list_coffees(session):
    print("Coffees we know about:")
    return list_objects(session, Coffee)


def list_brews(session):
    print("All brews:")
    return list_objects(session, Brew)


def create_roaster(session) -> int:
    name = input("What's this roaster called?\n")
    loc = input("Where's this roaster from?\n")
    new_roaster = Roaster(name=name, location=loc)
    session.add(new_roaster)
    session.flush()
    session.refresh(new_roaster)
    return new_roaster.id


def create_coffee(session):
    print(
        "Which roaster is this coffee from? If you don't see your roaster just press enter.\n"
    )
    valid_roasters = list_roasters(session)
    roaster_id = input()
    if roaster_id == "":
        roaster_id = create_roaster(session)
    else:
        try:
            roaster_int = int(roaster_id)
        except ValueError:
            roaster_int = "f"
        if roaster_int not in valid_roasters:
            print("Erm.. that's not a valid roaster.")
            create_coffee(session)

    name = input("Next, what's the name of the coffee?\n")
    new_line = "\n"
    roast = input(
        f"And finally, what's the roast?\n"
        f"{new_line.join([str(roast.value) + '. ' + roast.name for roast in Roast])}\n"
    )
    new_coffee = Coffee(name=name, roast=Roast(roast).name, roaster=roaster_id)
    session.add(new_coffee)
    session.flush()
    session.refresh(new_coffee)
    return new_coffee.id


def create_brew(session):
    print("Which coffee are we using?")
    valid_coffees = list_coffees(session)
    try:
        coffee_id = int(input())
    except ValueError:
        coffee_id = ""
    if coffee_id not in valid_coffees:
        print("Not a valid coffee. Try again!")
        create_brew(session)
    new_line = "\n"
    method = input(
        f"Which method are we using?\n{new_line.join([method.value + '. ' + method.name for method in Method])}\n"
    )
    grinder = input(
        f"Which grinder are we using?\n"
        f"{new_line.join([grinder.value + '. ' + grinder.name for grinder in Grinder])}\n"
    )
    grind_setting = input("What's the grind setting on the grinder?\n")
    temperature = int(input("What's temp is the water at?\n"))
    dose = float(input("How much coffee are you using (grams)?\n"))
    coffee_out = float(input("How much coffee did you get out (grams)?\n"))
    duration = input("How long was the brew?\n")
    thoughts = input("How's it taste? How'd the brew go?\n")

    new_brew = Brew(
        coffee=coffee_id,
        method=Method(method).name,
        grinder=Grinder(grinder).name,
        grind_setting=grind_setting,
        dose=dose,
        temperature=temperature,
        coffee_out=coffee_out,
        duration=duration,
        thoughts=thoughts,
    )
    session.add(new_brew)
    session.flush()
    session.refresh(new_brew)
    print(new_brew)
    return new_brew.id
