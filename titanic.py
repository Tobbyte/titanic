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


~ Made with ❤️ and without ai (unless otherwise disclaimed) or
  code completion (except intelliSense) ~


Todo:
    - use sanitize_data on all db accesses

"""


import sys
import webbrowser
from pathlib import Path

from config import (
    COMMANDS,
    SHIPS_MAP_PATH,
    SPEED_SYMBOL_HISTO,
    TOP_COUNTRIES_DEFAULT,
)
from data_handler import (
    get_count_of_field,
    get_data_by_field,
    get_data_by_field_value,
    get_data_fields,
    get_speed_data,
)
from fuzzy_tobbyte import get_similar
from helpers import (
    sanitize_data,
    scale_to_symbols,
    sort_dict_on_values,
)
from i_o import (
    get_ab_choice,
    get_menu_selection,
    get_user_input,
    get_user_input_options,
    print_pretty,
)
from mapping import draw_map as mapping_draw_map


def show_help() -> None:
    """Display the available commands."""
    print("\nAvailable commands:")

    help_items = {
        f"{command_item['command']}, {command_item['abbr']}": command_item[
            "desc"
        ]
        for command_item in COMMANDS.values()
    }

    print_pretty(help_items.items())
    print()  # spacer


def show_countries() -> None:
    """Print all countries present in data."""
    print("\nAll countries present in data [A-Z]:")
    by_country_sorted = sort_dict_on_values(get_count_of_field("COUNTRY"))
    print_pretty(by_country_sorted.items())
    print()  # spacer


def top_countries(num: int | None = None) -> None:
    """Print the top num countries by number of ships."""
    if not num:
        print(
            "No parameter for top_countries given, "
            f"defaulting to top {TOP_COUNTRIES_DEFAULT}",
        )
        num = TOP_COUNTRIES_DEFAULT
    print(f"\nThe top {num} countries by ships present in data:")
    ships_by_country_sorted = sort_dict_on_values(
        get_count_of_field("COUNTRY"),
    )
    ships_by_country_sorted_top = dict(
        list(ships_by_country_sorted.items())[:num],
    )

    print_pretty(ships_by_country_sorted_top.items())
    print()  # spacer


def ships_by_types() -> None:
    """Get num numbers of ships per types."""
    print("\nAll ship types present in data:")
    by_types_sorted = sort_dict_on_values(get_count_of_field("TYPE_SUMMARY"))
    print_pretty(by_types_sorted.items())
    print()  # spacer


def search_ship() -> None:
    """Search by name for ships.

    Uses custom fuzzy matching.
    """
    ship_names_list = get_data_by_field("SHIPNAME")
    ship_name_query = get_user_input("Name to search for (fuzzy): ").lower()
    search_res = get_similar(ship_names_list, ship_name_query)
    if not search_res:
        print(f'\nNo ship name in db matches your query "{ship_name_query}"')
    elif len(search_res) == 1:
        print(f"\nData of {ship_name_query}:")
        _print_ship_data(search_res[0])
    else:
        print("\nMultiple ships match your query, pick one:\n")
        numbered_results = {}
        for i in range(1, len(search_res) + 1):
            numbered_results[str(i)] = search_res[i - 1]
        prompt = "Select your choice by number: "
        choice = get_user_input_options(prompt, numbered_results)
        if choice == "-1":
            print()  # spacer
            return
        _print_ship_data(search_res[int(choice)])
    print()  # spacer


def _print_ship_data(ship_name: str) -> None:
    """Print data of a ship by ship name."""
    ships_data = get_data_by_field_value("SHIPNAME", ship_name)
    if not ships_data:
        print(f'\nNo ship name in db matches your query "{ship_name}"')
    else:
        print(f'\nShip data for "{ship_name}":\n')
        for ship in ships_data:
            print_pretty(ship.items())
    print()  # spacer


def list_data_fields() -> None:
    """List all fields of the ship database."""
    print("\nAll fields present in data:")
    fields = list(get_data_fields())
    fields.sort()
    print_pretty(dict.fromkeys(fields, " ").items())
    print()  # spacer


def show_speed_histogram() -> None:
    """Show a histogram of all ships speeds."""
    print(
        "\nAll ships speeds as histogram (descending).\n"
        "(Ships with 0 speed excluded):\n",
    )
    save_speed_data = {
        k: v
        for k, v in sanitize_data(get_speed_data(), float).items()
        if v is not None and v > 0
    }
    sorted_by_speed: dict[str, float] = dict(
        sorted(
            save_speed_data.items(),
            key=lambda item: item[1],
            reverse=True,
        ),
    )

    max_speed: float = max(sorted_by_speed.values())
    min_speed: float = min(sorted_by_speed.values())

    with_annotated_speed = {
        k: scale_to_symbols(v, min_speed, max_speed) * SPEED_SYMBOL_HISTO
        + " | "
        + str(v)
        for k, v in sorted_by_speed.items()
    }

    print_pretty(with_annotated_speed.items())
    print()  # spacer


def draw_map() -> None:
    """Create and opens a ships_map.html with ships position."""
    print("\nCreating ships_map.html in cwd.")
    mapping_draw_map()
    print()  # spacer
    open_map = get_ab_choice(
        'Do you want to open the map? Enter "(y)es" or "(n)o": ',
        "y",
        "n",
    )
    if open_map:
        webbrowser.open("file://" + str(Path(SHIPS_MAP_PATH).resolve()))
        print("\nShips map opened in new browser tap.")
    print()  # spacer


def quit_app() -> None:
    """Quit the program."""
    sys.exit()


def run_titanic() -> None:
    """Orchestrate the main program."""
    print(
        "\nWelcome to the Ships CLI! Enter 'help' to view available commands.",
    )
    show_help()
    menu_dispatch = {
        COMMANDS["help"]["command"]: show_help,
        COMMANDS["show_countries"]["command"]: show_countries,
        COMMANDS["top_countries"]["command"]: top_countries,
        COMMANDS["ships_by_types"]["command"]: ships_by_types,
        COMMANDS["search_ship"]["command"]: search_ship,
        COMMANDS["list_data_fields"]["command"]: list_data_fields,
        COMMANDS["show_speed_histogram"]["command"]: show_speed_histogram,
        COMMANDS["draw_map"]["command"]: draw_map,
        COMMANDS["quit"]["command"]: quit_app,
    }

    while True:
        choice, params = get_menu_selection()
        menu_dispatch[choice](*params)


if __name__ == "__main__":
    run_titanic()
