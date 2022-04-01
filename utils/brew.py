from datetime import timedelta

from utils.db import list_coffees, list_previous_brew_details
from utils.db_models import Grinder, Method, Brew, EspressoDetail
from utils.screen import clear_screen, prompt_method, NEW_LINE


def create_brew(session):
    new_espresso_detail = EspressoDetail()
    new_brew = Brew()
    clear_screen()
    print("Which coffee are we using?")
    valid_coffees = list_coffees(session)
    try:
        coffee_id = int(input())
    except ValueError:
        coffee_id = ""
    if coffee_id not in valid_coffees:
        print("Not a valid coffee. Try again!")
        create_brew(session)
    is_half_caff = True if input("Is this brew half-caff (blank for nah)? ") else False
    clear_screen()
    method_key = prompt_method()
    espresso_mode = method_key in ("3", "4")
    method = Method(method_key).name
    clear_screen()
    if espresso_mode:
        print(
            """Entering
███████████████████████████████████████████████████████████████████████████™
█▄─▄▄─█─▄▄▄▄█▄─▄▄─█▄─▄▄▀█▄─▄▄─█─▄▄▄▄█─▄▄▄▄█─▄▄─███▄─▀█▀─▄█─▄▄─█▄─▄▄▀█▄─▄▄─█
██─▄█▀█▄▄▄▄─██─▄▄▄██─▄─▄██─▄█▀█▄▄▄▄─█▄▄▄▄─█─██─████─█▄█─██─██─██─██─██─▄█▀█
▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▀▀▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▀▀▀▄▄▄▀▄▄▄▀▄▄▄▄▀▄▄▄▄▀▀▄▄▄▄▄▀"""
        )
    previous_brew = list_previous_brew_details(coffee_id, method, session)
    grinder = (
        input(
            f"Which grinder are we using?\n"
            f"{NEW_LINE.join([grinder.value + '. ' + grinder.name for grinder in Grinder])}\n"
        )
        or Grinder[previous_brew.grinder].value
    )
    grind_setting = (
        input("What's the grind setting on the grinder?\n")
        or previous_brew.grind_setting
    )
    temperature = int(
        input("What's temp is the water at?\n") or previous_brew.temperature
    )
    dose = float(
        input("How much coffee are you using (grams)?\n") or previous_brew.dose
    )
    if espresso_mode:
        try:
            preinfusion_seconds = int(
                input(
                    "How many seconds of preinfusion are we doing (leave blank for 0)?\n"
                )
                or 0
            )
            preinfusion_duration = str(timedelta(seconds=preinfusion_seconds))
            ratio_str = (
                input(
                    "What ratio are you aiming for (press enter for 1:2.5)?\n"
                ).strip()
                or "1:2.5"
            )
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
    thoughts = (
        input("How's it taste? How'd the brew go?\n")
        or "I left this blank because there wasn't much to say."
    )

    new_brew.coffee = coffee_id
    new_brew.is_half_caff = is_half_caff
    new_brew.method = method
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

    if espresso_mode:
        new_espresso_detail.brew = new_brew.id
        session.add(new_espresso_detail)
        session.flush()
    return new_brew.id
