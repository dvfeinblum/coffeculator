from datetime import timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.db_models import Coffee, Roaster, Method, Brew, Grinder, Roast


NEW_LINE = "\n"


def get_session():
    engine = create_engine(
        "postgresql://postgres:postgres@localhost:5432/coffeeculator"
    )
    session = sessionmaker(engine)
    return session()


def prompt_method():
    return input(
        f"Which method are we using?\n{NEW_LINE.join([method.value + '. ' + method.name for method in Method])}\n"
    )


def list_roasters(session):
    print("Roasters we know about:")
    ids = []
    for obj in session.query(Roaster):
        obj_id = obj.id
        ids.append(obj_id)
        print(f"{obj_id}. {obj}")
    return ids


def list_coffees(session):
    ids = []
    for coffee, roaster in session.query(Coffee, Roaster).join(Roaster):
        coffee_id = coffee.id
        ids.append(coffee_id)
        print(f"{coffee_id}. {coffee} from {roaster}")
    return ids


def list_brews(session):
    try:
        method = Method(prompt_method()).name
    except AttributeError:
        print("Not a valid method.")
        exit(1)
    ids = []
    for obj in session.query(Brew).filter(Brew.method == method):
        obj_id = obj.id
        ids.append(obj_id)
        print(f"{obj_id}. {obj}")
    return ids


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
    roast = input(
        f"And finally, what's the roast?\n"
        f"{NEW_LINE.join([str(roast.value) + '. ' + roast.name for roast in Roast])}\n"
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
    method = prompt_method()
    espresso_mode = method in ("3", "4")
    if espresso_mode:
        print(
            """Entering\n
███████████████████████████████████████████████████████████████████████████
█▄─▄▄─█─▄▄▄▄█▄─▄▄─█▄─▄▄▀█▄─▄▄─█─▄▄▄▄█─▄▄▄▄█─▄▄─███▄─▀█▀─▄█─▄▄─█▄─▄▄▀█▄─▄▄─█
██─▄█▀█▄▄▄▄─██─▄▄▄██─▄─▄██─▄█▀█▄▄▄▄─█▄▄▄▄─█─██─████─█▄█─██─██─██─██─██─▄█▀█
▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▀▀▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▀▀▀▄▄▄▀▄▄▄▀▄▄▄▄▀▄▄▄▄▀▀▄▄▄▄▄▀\n"""
        )
    grinder = input(
        f"Which grinder are we using?\n"
        f"{NEW_LINE.join([grinder.value + '. ' + grinder.name for grinder in Grinder])}\n"
    )
    grind_setting = input("What's the grind setting on the grinder?\n")
    temperature = int(input("What's temp is the water at?\n"))
    dose = float(input("How much coffee are you using (grams)?\n"))
    if espresso_mode:
        try:
            coffee_mass, out_mass = (
                input("What ratio are you aiming for (coffee in:coffee out)?\n")
                .strip()
                .split(":")
            )
            target_mass = dose * float(out_mass) / float(coffee_mass)
            print(
                f"Okay; you should be aiming for {target_mass}. Good luck with the brew!"
            )
        except ValueError:
            print("Aight I can't help you good luck.")
    coffee_out = float(input("How much coffee did you get out (grams)?\n"))
    if espresso_mode:
        duration_seconds = int(input("How many seconds was the brew?\n"))
        duration = str(timedelta(seconds=duration_seconds))
    else:
        duration = input("How long was the brew (hh:mm:ss)?\n")
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
