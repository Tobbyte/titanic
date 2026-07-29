"""A simple CLI to interact with data from MarineTraffic.

help
    Prints a list of the available commands.
show_countries
    Prints a list of all the countries of the ships, without duplicates.
    The countries should be ordered alphabetically.
top_countries <num_countries>
    Prints a list of top countries with the most ships.
    For example, top_countries 5, prints a list of the 5 countries which
    have the most ships, along with the number of ships.

"""

import json
from pathlib import Path

DATA_PATH = "ships_data.json"
TOP_COUNTRIES_DEFAULT = 5
COMMANDS = {
    ("help", "h"): ("", "Show this help"),
    "show_countries": ("", "List all countries"),
    "top_countries": (
        "<num_countries>",
        f"Show top countries [default: {TOP_COUNTRIES_DEFAULT}]",
    ),
}


def _load_data() -> dict:
    with Path.open(Path(DATA_PATH)) as file:
        return json.loads(file.read())


def show_help() -> None:
    print("\nAvailable commands:")
    commands_items = COMMANDS.items()
    max_width = max(len(k[0] + v[0]) for k, v in commands_items)
    for comm, param in commands_items:
        param_a, param_b = param
        print(f"    {comm[0] + ' ' + param_a:<{max_width + 4}}", param_b)
    print()  # spacer


def show_countries() -> None:
    data: list[dict] = _load_data()["data"]
    countries = {d["COUNTRY"] for d in data}
    for c in countries:
        print(c)


def top_countries(num: int | None = None) -> None:
    if not num:
        print(
            "No parameter for top_countries given, "
            f"defaulting to top {TOP_COUNTRIES_DEFAULT}",
        )
        num = TOP_COUNTRIES_DEFAULT
    print(f"top_countries({num})")


def _get_menu_selection() -> tuple[str, tuple]:
    """Presents the cli.

    Returns a tuple[str, tuple] representing the selected
    menu command and entered parameters (if any).
    Return a second tuple bc it unpacks into "nothing" if empty.
    f.e.
    "help" -> ("help", ())
    "top_countries 5" -> ("top_countries", ("5"))
    """
    while True:
        raw_user_input = input("Enter command: ")
        user_input_lst = raw_user_input.split()
        command = user_input_lst[0]
        param = user_input_lst[1:2]  # slice for i1 to prevent out-of-index
        if command not in COMMANDS:
            print("Unknown command. See 'help' for all available commands.")
        else:
            return command, tuple(param)


def run_titanic() -> None:
    print(
        "\nWelcome to the Ships CLI! "
        "Enter 'help' to view available commands.\n",
    )
    command_fn = [
        show_help,
        show_countries,
        top_countries,
    ]
    menu_dispatch = dict(zip(COMMANDS.keys(), command_fn, strict=True))
    choice, params = _get_menu_selection()
    menu_dispatch[choice](*params)


def main() -> None:
    run_titanic()


if __name__ == "__main__":
    main()
