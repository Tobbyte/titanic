"""Mapping module using Folium."""

import folium
from data_handler import get_all_data


def add_popups(m: folium.Map) -> list[folium.GeoJsonPopup]:
    popup = folium.GeoJsonPopup(
        fields=["SHIPNAME"],
        localize=True,
        labels=True,
        style="background-color: yellow;",
    )
    return [popup]


def add_tooltips(m: folium.Map) -> list[folium.GeoJsonTooltip]:
    tooltip = folium.GeoJsonTooltip(
        fields=["SHIPNAME"],
        aliases=["hurtz"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
        max_width=800,
    )
    return [tooltip]


# def add_markers(m: folium.Map) -> None:
#     group_1 = folium.FeatureGroup("first group").add_to(m)
#     folium.Marker((70, 73), icon=folium.Icon("red")).add_to(group_1)
#     folium.Marker((69, 70), icon=folium.Icon("red")).add_to(group_1)

#     group_2 = folium.FeatureGroup("second group").add_to(m)
#     folium.Marker((68, 68), icon=folium.Icon("green")).add_to(group_2)


# def add_polyline(m: folium.Map) -> folium.PolyLine:
#     trail_coordinates = [
#         (71.351871840295871, 73.655963711222626),
#         (71.374144382613707, 73.719861619751498),
#         (71.391042575973145, 73.784922248007007),
#         (71.400964450973134, 73.851042243124397),
#         (71.402411391077322, 74.050048183880477),
#     ]
#     return folium.PolyLine(trail_coordinates, tooltip="Coast")


def construct_geojson(data: list) -> dict:
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
    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    return geojson


def get_latlng(data: list) -> list[tuple[str, str]]:
    return [
        (datapoint["LAT"], datapoint["LON"])
        for datapoint in data
        if "LON" in datapoint and "LAT" in datapoint
    ]


def init_map() -> None:
    raw_data = get_all_data()

    all_latlng = get_latlng(raw_data["data"])

    # sanitize latlngs
    # get_bounds()
    # get_center()

    m = folium.Map(location=[71.38, 73.9], zoom_start=5)
    # add_markers(m)
    tooltip = add_tooltips(m)[0]
    popup = add_popups(m)[0]

    all_ships_geojson = construct_geojson(raw_data["data"])
    folium.GeoJson(
        all_ships_geojson,
        name="hello world",
        tooltip=tooltip,
        popup=popup,
    ).add_to(m)

    # polyline = add_polyline(m)
    # polyline.add_to(m)

    folium.LayerControl().add_to(m)

    m.save("index.html")

if __name__ == "__main__":
    init_map()
