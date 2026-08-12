"""Apps constants."""
TOP_COUNTRIES_DEFAULT = 5
SPEED_SYMBOL_HISTO = "▀"  # U+2580
MAX_SYMBOLS_HISTO = 100
DATA_PATH = "ships_data.json"


COMMANDS = {
    "help": ("help", "h"),
    "show_countries": ("show_countries", "sc"),
    "top_countries": ("top_countries", "tc"),
    "ships_by_types": ("ships_by_types", "sbt"),
    "search_ship": ("search_ship", "ss"),
    "list_data_fields": ("list_data_fields", "ldf"),
    "show_speed_histogram": ("show_speed_histogram", "sh"),
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
    "search_ship": ("search_ship, ss", "Search ships by name (fuzzy)."),
    "list_data_fields": (
        "list_data_fields, ldf",
        "List all fields of ship db.",
    ),
    "show_speed_histogram": (
        "show_speed_histogram, sh",
        "Show a histogram of all ships speeds.",
    ),
    "quit": ("quit, q", "Quit the program"),
}
