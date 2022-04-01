import os

from utils.db_models import Method

NEW_LINE = "\n"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")  # nosec


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
