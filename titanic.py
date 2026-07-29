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
    "help": ("help", "h"),
    "show_countries": ("show_countries", "sc"),
    "top_countries": ("top_countries", "tc"),
}

COMMANDS_DESCRIPTION = {
    "help": ("help", "Show this help"),
    "show_countries": ("show_countries", "List all countries"),
    "top_countries": (
        "top_countries <num_countries>",
        f"Show top countries [default: {TOP_COUNTRIES_DEFAULT}]",
    ),
}


def _load_data() -> dict:
    with Path.open(Path(DATA_PATH)) as file:
        return json.loads(file.read())


def show_help() -> None:
    print("\nAvailable commands:")

    command_desc_vals = COMMANDS_DESCRIPTION.values()
    max_width = max(len(c) for c, _ in command_desc_vals)

    for comm, desc in command_desc_vals:
        print(f"    {comm:<{max_width + 4}} {desc}")
    print()  # spacer

def get_top_countries(num: int):
    data: list[dict] = _load_data()["data"]
    countries = {}
    # extract num of ships per country
    for ship in data:
        ship_origin = ship["COUNTRY"]
        countries[ship_origin] = countries.get(ship_origin, 0) + 1
    # sort by num of ships

    sort = sorted(countries.items(), key=lambda item: item[1], reverse=True)
    return dict(sort[:num])

def show_countries() -> None:
    print("\nAll countries present in data [A-Z]:")
    data: list[dict] = _load_data()["data"]
    countries = sorted({d["COUNTRY"] for d in data})
    for c in countries:
        print(c)


def top_countries(num: int | None = None) -> None:
    if not num:
        print(
            "No parameter for top_countries given, "
            f"defaulting to top {TOP_COUNTRIES_DEFAULT}",
        )
        num = TOP_COUNTRIES_DEFAULT
    print(f"\nThe top {num} countries by ships present in data:")
    ships_by_country = get_top_countries(num)
    max_length = max([len(c) for c in ships_by_country])
    for country, num_ships in ships_by_country.items():
        print(f"{country:<{max_length + 2}}: {num_ships}")


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
        elif not all(para.isdigit() for para in param):
            print("Parameter must be an integer.")
        else:
            return command, tuple(int(p) for p in param)


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
