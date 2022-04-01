#!/usr/bin/env python3
from utils.brew import create_brew
from utils.db import (
    get_session,
    list_coffees,
    create_coffee,
    list_roasters,
    create_roaster,
    list_brews,
    list_metrics,
)

CHOICES = [
    create_brew,
    list_coffees,
    list_roasters,
    create_coffee,
    create_roaster,
    list_brews,  # lil debug tool
]


if __name__ == "__main__":
    sesh = get_session()
    print(
        f"Heyo, welcome to the"
        """
█▀▀ █▀▀█ █▀▀ █▀▀ █▀▀ █▀▀ █▀▀ █░░█ █░░ █▀▀█ ▀▀█▀▀ █▀▀█ █▀▀█™
█░░ █░░█ █▀▀ █▀▀ █▀▀ █▀▀ █░░ █░░█ █░░ █▄▄█ ░░█░░ █░░█ █▄▄▀
▀▀▀ ▀▀▀▀ ▀░░ ▀░░ ▀▀▀ ▀▀▀ ▀▀▀ ░▀▀▀ ▀▀▀ ▀░░▀ ░░▀░░ ▀▀▀▀ ▀░▀▀"""
    )
    list_metrics(sesh)
    print(
        "How about you tell me what you'd like to do?\n"
        "1 - List Coffees\n"
        "2 - List Roasters\n"
        "3 - Create Coffee\n"
        "4 - Create Roaster\n"
        f"To start a new brew, just press enter!"
    )
    try:
        usr_choice = int(input())
    except ValueError:
        usr_choice = 0
    print("\033[A                             \033[A")
    CHOICES[usr_choice](sesh)
    sesh.commit()
