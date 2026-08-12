"""Apps constants."""
TOP_COUNTRIES_DEFAULT = 5
SPEED_SYMBOL_HISTO = "▀"  # U+2580
MAX_SYMBOLS_HISTO = 100
DATA_PATH = "ships_data.json"

COMMANDS = {
    # command is what the user calls
    # abbr is an alternative (gets converted to command)
    # desc is what's in the help
    "help": {
        "command": "help",
        "abbr": ("h"),
        "desc": "Show this help",
    },
    "show_countries": {
        "command": "show_countries",
        "abbr": ("sc"),
        "desc": "List all countries",
    },
    "top_countries": {
        "command": "top_countries",
        "abbr": ("tc"),
        "desc": f"Show top countries (default:){TOP_COUNTRIES_DEFAULT}]",
    },
    "ships_by_types": {
        "command": "ships_by_types",
        "abbr": ("sbt"),
        "desc": "List ships by types.",
    },
    "search_ship": {
        "command": "search_ship",
        "abbr": ("ss"),
        "desc": "Search ships by name (fuzzy).",
    },
    "list_data_fields": {
        "command": "list_data_fields",
        "abbr": ("ldf"),
        "desc": "List all fields of ship db.",
    },
    "show_speed_histogram": {
        "command": "show_speed_histogram",
        "abbr": ("sh"),
        "desc": "Show a histogram of all ships speeds.",
    },
    "quit": {
        "command": "quit",
        "abbr": ("q"),
        "desc": "Quit the program",
    },
}
