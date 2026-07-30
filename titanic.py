"""A simple CLI to interact with data from MarineTraffic.

help
    Prints a list of the available commands.
show_countries
    Prints a list of all countries of the ships, without duplicates,
    ordered alphabetically.
top_countries <num_countries>
    Prints a list of the top <num> countries with the most ships.
    For example, top_countries 5, prints a list of the 5 countries which
    have the most ships, along with the number of ships.
quit
    Quits the program.


~ Made with ❤️ and without ai or code completion (except intelliSense) ~

"""

import json
import sys
from collections.abc import Iterable
from pathlib import Path

DATA_PATH = "ships_data.json"
TOP_COUNTRIES_DEFAULT = 5
COMMANDS = {
    "help": ("help", "h"),
    "show_countries": ("show_countries", "sc"),
    "top_countries": ("top_countries", "tc"),
    "ships_by_types": ("ships_by_types", "sbt"),
    "seach_ship": ("seach_ship", "ss"),
    "quit": ("quit", "q"),
}

COMMANDS_DESCRIPTION = {
    "help": ("help, h", "Show this help"),
    "show_countries": ("show_countries, sc", "List all countries"),
    "top_countries": (
        "top_countries, tc <num_countries>",
        f"Show top countries [default: {TOP_COUNTRIES_DEFAULT}]",
    ),
    "ships_by_types": ("ships_by_types, sbt", "List ships by types."),
    "seach_ship": ("seach_ship", "Search ships by name (fuzzy)."),
    "quit": ("quit, q", "Quit the program"),
}


def _load_data() -> dict:
    # read the data json
    with Path.open(Path(DATA_PATH)) as file:
        return json.loads(file.read())


def show_help() -> None:
    """Display the available commands."""
    print("\nAvailable commands:")

    command_desc_vals = COMMANDS_DESCRIPTION.values()
    _print_pretty(command_desc_vals)
    print()  # spacer


def _sort_dict_on_values(
    unsorted_dict: dict,
    *,
    descending: bool = True,
) -> dict:
    return dict(
        sorted(
            unsorted_dict.items(),
            key=lambda item: item[1],
            reverse=descending,
        ),
    )


def get_top_countries() -> dict:
    """Get num numbers of ships per country."""
    data: list[dict] = _load_data()["data"]
    countries = {}

    # extract num of ships per country
    for ship in data:
        ship_origin = ship["COUNTRY"]
        countries[ship_origin] = countries.get(ship_origin, 0) + 1

    return countries


def get_ships_by_types() -> dict:
    """Get num numbers of ships per types."""
    data: list[dict] = _load_data()["data"]
    types = {}

    for ship in data:
        ship_type = ship["TYPE_SUMMARY"]
        types[ship_type] = types.get(ship_type, 0) + 1

    return types


def ships_by_types() -> None:
    """Get num numbers of ships per types."""
    print("\nAll ship types present in data:")
    by_types_sorted = _sort_dict_on_values(get_ships_by_types())
    _print_pretty(by_types_sorted.items())
    print()  # spacer


def show_countries() -> None:
    """Print all countries present in data."""
    print("\nAll countries present in data [A-Z]:")
    data: list[dict] = _load_data()["data"]
    countries = sorted({d["COUNTRY"] for d in data})
    for country in countries:
        print("    " + country)
    print()  # spacer


def search_ship() -> None:
    """Search by name for ships.

    Uses custom fuzzy matching.
    """
    print("search_ship()")


def top_countries(num: int | None = None) -> None:
    """Print the top num countries by number of ships."""
    if not num:
        print(
            "No parameter for top_countries given, "
            f"defaulting to top {TOP_COUNTRIES_DEFAULT}",
        )
        num = TOP_COUNTRIES_DEFAULT
    print(f"\nThe top {num} countries by ships present in data:")
    ships_by_country_sorted = _sort_dict_on_values(get_top_countries())
    ships_by_country_sorted_top = dict(  # extract?
        list(ships_by_country_sorted.items())[: num + 1],
    )

    _print_pretty(ships_by_country_sorted_top.items())
    print()  # spacer


def _resolve_command(user_command: str) -> str | None:
    # Resolve a abbreviation like "h" to its command.
    for command, variants in COMMANDS.items():
        if user_command in variants:
            return command
    return None


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
        user_command = user_input_lst[0]
        param = user_input_lst[1:2]  # slice for i1 to prevent out-of-index
        command = _resolve_command(user_command)
        if not command:
            print("Unknown command. See 'help' for all available commands.")
        elif not all(para.isdigit() for para in param):
            print("Parameter must be an integer.")
        else:
            return command, tuple(int(p) for p in param)


def _print_pretty(items: Iterable) -> None:
    """Pretty print a list of key:value pairs.

    Calculates the max length of the key to align the
    values that length +2 to the right.
    """
    max_width = max(len(c) for c, _ in items)
    for comm, desc in items:
        print(f"    {comm:<{max_width + 4}} {desc}")


def quit_app() -> None:
    """Quit the program."""
    sys.exit()


def run_titanic() -> None:
    """Orchestrate the main program."""
    print(
        "\nWelcome to the Ships CLI! "
        "Enter 'help' to view available commands.\n",
    )
    command_fn = [
        show_help,
        show_countries,
        top_countries,
        ships_by_types,
        search_ship,
        quit_app,
    ]
    menu_dispatch = dict(zip(COMMANDS.keys(), command_fn, strict=True))
    while True:
        choice, params = _get_menu_selection()
        menu_dispatch[choice](*params)


if __name__ == "__main__":
    run_titanic()
