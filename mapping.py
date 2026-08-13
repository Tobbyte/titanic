"""Mapping module using Folium."""

import folium
from config import COLOR_LEGEND_FILLER, FOLIUM_COLOR_OPTIONS, SHIPS_MAP_PATH
from data_handler import get_all_data, get_data_by_field, get_data_fields_save
from helpers import sanitize_data


def _popup(field_names: list) -> folium.GeoJsonPopup:
    """Construct popup object."""
    return folium.GeoJsonPopup(
        fields=field_names,
    )


def _tooltip(
    field_names: list,
    field_names_alias: list,
) -> folium.GeoJsonTooltip:
    """Construct tooltip object."""
    return folium.GeoJsonTooltip(
        fields=field_names,
        aliases=field_names_alias,
        sticky=False,
        max_width=800,
    )


def construct_geojson(data: list) -> dict:
    """Construct a GeoJSON json from the data."""
    features = [
        {
            "properties": dict(ship),
            "id": ship["SHIP_ID"],
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [ship["LON"], ship["LAT"]],
            },
        }
        for ship in data
        if "SHIP_ID" in ship and "LON" in ship and "LAT" in ship
    ]
    return {
        "type": "FeatureCollection",
        "features": features,
    }


def get_latlng(data: list) -> dict[str, list]:
    """Get all latitudes and longitudes from the data.

    Sanitizes LAT, LON fields to floats.
    """
    san_data = [
        sanitize_data(d, float, only_fields=["LAT", "LON"]) for d in data
    ]

    res = {"lats": [], "lngs": []}

    for d in san_data:
        if d["LAT"] is not None and d["LON"] is not None:
            res["lats"].append(d["LAT"])
            res["lngs"].append(d["LON"])
    return res


def _get_data_bounds(data_list: list) -> dict[str, list[float]]:
    """Get the bounding box (ne, sw) and center of the data points."""
    latlng_list: dict = get_latlng(data_list)
    lats = latlng_list["lats"]
    lngs = latlng_list["lngs"]

    center = [(min(lats) + max(lats)) / 2, (min(lngs) + max(lngs)) / 2]
    return {
        "ne": [max(lats), max(lngs)],
        "sw": [min(lats), min(lngs)],
        "center": center,
    }


def _assign_color(types: list) -> dict:
    """Assign colors to ship types."""
    # assumes len(types) <= FOLIUM_COLOR_OPTIONS. Enough for now.
    return dict(zip(types, FOLIUM_COLOR_OPTIONS, strict=False))

def draw_map() -> None:
    """Create and save a folium map."""
    raw_data = get_all_data()

    all_fields = get_data_fields_save()
    data_bounds = _get_data_bounds(raw_data["data"])

    m = folium.Map(
        location=data_bounds["center"],
        zoom_start=2,
    )

    ship_types = list(set(get_data_by_field("TYPE_SUMMARY")))
    types_colors = _assign_color(ship_types)

    for s_type in ship_types:
        type_data = [
            d for d in raw_data["data"] if d["TYPE_SUMMARY"] == s_type
        ]
        colored_name = (
            f"<span style='background-color: {types_colors[s_type]};'>"
            f"{COLOR_LEGEND_FILLER}</span><span> {s_type}</span>"
        )
        folium.GeoJson(
            construct_geojson(type_data),
            name=colored_name,
            tooltip=_tooltip(["SHIPNAME"], ["ship name: "]),
            popup=_popup(list(all_fields)),
            marker=folium.Marker(icon=folium.Icon(color=types_colors[s_type])),
        ).add_to(m)

    # not using because optics - all ships box to big (what she said).
    # could be solved by using weighted box for bounds instead of all?
    # won't fix
    #  m.fit_bounds(
    #     [data_bounds["sw"], data_bounds["ne"]], # noqa: ERA001
    # ) # noqa: ERA001

    folium.LayerControl(collapsed=False).add_to(m)  # should be added at last

    m.save(SHIPS_MAP_PATH)

if __name__ == "__main__":
    draw_map()
