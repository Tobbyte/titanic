# Ships CLI

A simple cli to explore and analyze ship data from MarineTraffic (local file for now).

## Features

- Search ships by name (fuzzy matching, using custom module [fuzzy_tobbyte](https://github.com/Tobbyte/fuzzy_tobbyte))
- View top countries by ship count
- Display ship types and speeds
- Interactive map visualization
- Data filtering and field inspection

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```bash
python titanic.py
```

Available commands:
- `help` / `h` — Show available commands
- `show_countries` / `sc` — List all countries
- `top_countries <num>` / `tc` — Show top N countries by ships
- `ships_by_types` / `sbt` — List ships by type
- `search_ship` / `ss` — Search ships by name
- `list_data_fields` / `ldf` — Show all database fields
- `show_speed_histogram` / `sh` — Display speed histogram
- `draw_map` / `dm` — Generate interactive map
- `quit` / `q` — Exit

## Requirements

See `requirements.txt` for dependencies (folium, fuzzy_tobbyte).


## Disclaimer
This readme is ai generated