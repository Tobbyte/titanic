"""Helper functions."""
from config import MAX_SYMBOLS_HISTO


def sort_dict_on_values(
    unsorted_dict: dict,
    *,
    descending: bool = True,
) -> dict:
    """Sort a dict on its values."""
    return dict(
        sorted(
            unsorted_dict.items(),
            key=lambda item: item[1],
            reverse=descending,
        ),
    )


def sanitize_data(
    raw_data: dict,
    expected_type: type[float] | type[int] | type[str],
) -> dict:
    """Sanitize all fields of to match provided type.

    Replaces non-convertible data with None.
    """
    sanitized_data: dict = {}
    for key, value in raw_data.items():
        if expected_type is int:
            try:
                sanitized_data[key] = int(value)
            except ValueError:
                sanitized_data[key] = None
        elif expected_type is float:
            try:
                sanitized_data[key] = float(value)
            except ValueError:
                sanitized_data[key] = None
        elif expected_type is str:
            sanitized_data[key] = str(value)
        else:
            e_msg = "Expected type must be float or str."
            raise ValueError(e_msg)
    return sanitized_data


### Disclaimer: An AI helped with coming up with this formula.
def scale_to_symbols(
    value: float,
    min_value: float,
    max_value: float,
) -> int:
    """Scale value to a symbol count between 1 and max_symbols."""
    if max_value == min_value:
        return MAX_SYMBOLS_HISTO
    fraction = (value - min_value) / (max_value - min_value)
    return 1 + round(fraction * (MAX_SYMBOLS_HISTO - 1))
    ### End AI help.


def is_valid_int(raw_input: str) -> bool:
    """Check if a string can be converted to an int."""
    try:
        int(raw_input)
    except ValueError:
        return False
    return True
