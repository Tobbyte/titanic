"""Input_Output related methods."""
from collections.abc import Iterable

from config import COMMANDS
from helpers import is_valid_int


def get_user_input_options(prompt: str, options: dict) -> str:
    """Get user input from a dict of valid options.

    Returns str which is key of options input.
    """
    valid_inputs = [k for k, v in options.items()]
    exit_msg = "\n(Enter to exit) "
    print()  # spacer
    print_pretty(options.items())
    print()  # spacer
    while True:
        raw_input = input(prompt + exit_msg).strip()
        if not raw_input:
            return "-1"
        if not is_valid_int(raw_input) or raw_input not in valid_inputs:
            valid_inputs_int = [int(v) for v in valid_inputs]
            print(
                f"\nNot a valid input. Select ({min(valid_inputs_int)} - "
                f"{max(valid_inputs_int)})\n",
            )
        else:
            return raw_input


def get_user_input(prompt: str) -> str:
    """Get user input with a prompt."""
    while True:
        raw_input = input(prompt).strip()
        if not raw_input:
            print("Not a valid input")
        else:
            return raw_input


def get_ab_choice(prompt: str, opt_a: str, opt_b: str) -> bool:
    """Ask user to choose between opt_a and opt_b.

    Returns True for opt_a,
    returns False for opt_b.
    """
    while True:
        choice = get_user_input(prompt)
        if choice not in (opt_a, opt_b):
            print(f'Choose "{opt_a}" or "{opt_b}": ')
        else:
            break

    return choice == opt_a


def resolve_command(user_command: str) -> str | None:
    """Resolve a abbreviation like "h" to its command."""
    for commands in COMMANDS.values():
        if (
            user_command == commands["command"]
            or user_command in commands["abbr"]
        ):
            return commands["command"]
    return None


def get_menu_selection() -> tuple[str, tuple]:
    """Presents the cli.

    Returns a tuple[str, tuple] representing the selected
    menu command and entered parameters (if any).
    Return a second tuple bc it unpacks into "nothing" if empty.
    f.e.
    "help" -> ("help", ())
    "top_countries 5" -> ("top_countries", ("5"))
    """
    insist_to_quit = False
    while True:
        raw_user_input = input("Enter command: ").lower()
        if not raw_user_input:
            print("Press Enter again to exit.")
            if insist_to_quit:
                return ("quit", ())
            insist_to_quit = True
            continue

        insist_to_quit = False
        user_input_lst = raw_user_input.split()
        user_command = user_input_lst[0]
        param = user_input_lst[1:2]  # slice for i1 to prevent out-of-index
        command = resolve_command(user_command)
        if not command:
            print("Unknown command. See 'help' for all available commands.")
        elif not all(para.isdigit() for para in param):
            print("Parameter must be an integer.")
        else:
            return command, tuple(int(p) for p in param)


def print_pretty(items: Iterable) -> None:
    """Pretty print a list of key:value pairs.

    Calculates the max length of the key to align the
    values that length +2 to the right.
    """
    max_width = max(len(c) for c, _ in items)
    for comm, desc in items:
        print(f"    {comm:<{max_width + 4}} {desc}")
