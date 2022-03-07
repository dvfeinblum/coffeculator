from datetime import timedelta
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.db_models import (
    Coffee,
    Roaster,
    Method,
    Brew,
    Grinder,
    Roast,
    EspressoDetail,
)

NEW_LINE = "\n"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")  # nosec


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


def list_and_print_query_results(result_set):
    ids = []
    for obj in result_set:
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


def list_roasters(session):
    return list_and_print_query_results(session.query(Roaster))


def list_brews(session):
    try:
        method = Method(prompt_method()).name
        return list_and_print_query_results(
            session.query(Brew).filter(Brew.method == method)
        )
    except AttributeError:
        print("Not a valid method.")
        exit(1)


def create_roaster(session) -> int:
    clear_screen()
    name = input("What's this roaster called?\n")
    loc = input("Where's this roaster from?\n")
    new_roaster = Roaster(name=name, location=loc)
    session.add(new_roaster)
    session.flush()
    session.refresh(new_roaster)
    return new_roaster.id


def create_coffee(session):
    clear_screen()
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
    new_espresso_detail = EspressoDetail()
    new_brew = Brew()
    print("Which coffee are we using?")
    valid_coffees = list_coffees(session)
    try:
        coffee_id = int(input())
    except ValueError:
        coffee_id = ""
    if coffee_id not in valid_coffees:
        print("Not a valid coffee. Try again!")
        create_brew(session)
    clear_screen()
    method = prompt_method()
    espresso_mode = method in ("3", "4")
    clear_screen()
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
            preinfusion_seconds = int(
                input("How many seconds of preinfusion are we doing?\n")
            )
            preinfusion_duration = str(timedelta(seconds=preinfusion_seconds))
            ratio_str = input(
                "What ratio are you aiming for (coffee in:coffee out)?\n"
            ).strip()
            new_espresso_detail.ratio = ratio_str
            new_espresso_detail.preinfusion_duration = preinfusion_duration

            coffee_mass, out_mass = ratio_str.split(":")
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

    new_brew.coffee = coffee_id
    new_brew.method = Method(method).name
    new_brew.grinder = Grinder(grinder).name
    new_brew.grind_setting = grind_setting
    new_brew.dose = dose
    new_brew.temperature = temperature
    new_brew.coffee_out = coffee_out
    new_brew.duration = duration
    new_brew.thoughts = thoughts

    session.add(new_brew)
    session.flush()
    session.refresh(new_brew)
    print(new_brew)

    if espresso_mode:
        new_espresso_detail.brew = new_brew.id
        session.add(new_espresso_detail)
        session.flush()
        print(new_espresso_detail)
    return new_brew.id
