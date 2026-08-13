"""Mapping module using Folium."""

import folium

geoJson = {
    "type": "FeatureCollection",
    "features": [
        {
            "properties": {"name": "Alabama"},
            "id": "AL",
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[68.359296, 75.00118]]],
            },
        },
        {
            "properties": {"name": "Alaska"},
            "id": "AK",
            "type": "Feature",
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [[[[73.602021, 72.117982]]]],
            },
        },
    ],
}


m = folium.Map(location=[71.38, 73.9], zoom_start=5)


group_1 = folium.FeatureGroup("first group").add_to(m)
folium.Marker((70, 73), icon=folium.Icon("red")).add_to(group_1)
folium.Marker((69, 70), icon=folium.Icon("red")).add_to(group_1)

group_2 = folium.FeatureGroup("second group").add_to(m)
folium.Marker((68, 68), icon=folium.Icon("green")).add_to(group_2)


trail_coordinates = [
    (71.351871840295871, 73.655963711222626),
    (71.374144382613707, 73.719861619751498),
    (71.391042575973145, 73.784922248007007),
    (71.400964450973134, 73.851042243124397),
    (71.402411391077322, 74.050048183880477),
]

folium.PolyLine(trail_coordinates, tooltip="Coast").add_to(m)


folium.GeoJson(geoJson, name="hello world").add_to(m)

folium.LayerControl().add_to(m)

m.save("index.html")
