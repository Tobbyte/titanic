"""Datahandler for db related actions."""
import json
from pathlib import Path

from config import DATA_PATH

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH_ABS = BASE_DIR / DATA_PATH

def _load_data() -> dict:
    # read the data json
    with Path(DATA_PATH_ABS).open() as file:
        return json.loads(file.read())


def get_count_of_field(field: str) -> dict:
    """Get count of unique values per field."""
    data: list[dict] = _load_data()["data"]
    filtered_data = {}

    for ship in data:
        field_data = ship[field]
        filtered_data[field_data] = filtered_data.get(field_data, 0) + 1

    return filtered_data


def get_data_by_field_value(field: str, query: str) -> list:
    """Get all data that has a specific value in a field."""
    data: list[dict] = _load_data()["data"]
    return [ship for ship in data if ship[field] == query]


def get_data_by_field(field: str) -> list:
    """Get all data of a specific field."""
    data: list[dict] = _load_data()["data"]
    return [ship[field] for ship in data]


def get_db_fields() -> set:
    """Get all unique keys of the db data."""
    data: list[dict[str, str]] = _load_data()["data"]
    uique_keys = set()
    for item in data:
        uique_keys.update(item.keys())
    return uique_keys


def get_speed_data() -> dict:
    """Get all ship names and their speed data."""
    data: list[dict] = _load_data()["data"]
    return {ship["SHIPNAME"]: ship["SPEED"] for ship in data}

def get_all_data() -> dict:
    return _load_data()
