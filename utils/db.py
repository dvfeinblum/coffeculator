from datetime import datetime

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from utils.db_models import (
    Coffee,
    Roaster,
    Method,
    Brew,
    Roast,
)
from utils.screen import (
    NEW_LINE,
    list_and_print_query_results,
    prompt_method,
    clear_screen,
)


def get_session():
    engine = create_engine(
        "postgresql://postgres:postgres@localhost:5432/coffeeculator"
    )
    session = sessionmaker(engine)
    return session()


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


def list_metrics(session):
    brew_cnt, tot_coffee, tot_brewtime = session.query(
        func.count(Brew.id),
        func.sum(Brew.coffee_out),
        func.sum(Brew.duration),
    ).all()[0]
    # I consider 15g of coffee to basically be equal to a single cup
    num_drinks_today = int(
        session.query(func.sum(Brew.dose))
        .where(Brew.date >= datetime.now().replace(hour=0, minute=0, second=0))
        .all()[0][0]
        / 15
    )
    print(
        f"We've made {brew_cnt} brews ({num_drinks_today} of which were made today), producing {int(tot_coffee)}g of "
        f"coffee in "
        f"{int(tot_brewtime.total_seconds()/60)} minutes.\n"
    )


def list_previous_brew_details(coffee_id, method, session) -> Brew:
    last_brew = (
        session.query(Brew)
        .filter(Brew.method == method, Brew.coffee == coffee_id)
        .order_by(Brew.id.desc())
        .first()
    )
    if last_brew:
        print(
            f"Here's some info about the last time we brewed this coffee.\n{last_brew}\n"
            f"If you'd like to reuse these settings, just press enter at each prompt.\n"
        )
    return last_brew


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
