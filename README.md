# Pokémon Finder (Streamlit + SQLite)

A **Streamlit** application that lets you search Pokémon by **name**, **type**, and **region**, showing:
- the Pokémon sprite
- its types
- the regions where it appears
- a Bulbapedia link
- and (when available) additional **non-default forms** (regional forms / mega evolutions / variants) with their own types and images.

This project also includes a simple data pipeline that builds a local **SQLite database** from:
- data fetched from **PokeAPI**
- custom region lists stored in plain text files

This project was built as a personal portfolio project to practice API integration, data processing and interactive app development.

---

## Features

- 🔎 Search by **partial name**
- 🧪 Filter by **type** (including forms types)
- 🗺️ Filter by **region** (Kanto → Paldea)
- 🖼️ Display Pokémon images
- 🔗 External reference link to **Bulbapedia**
- ⚠️ Detect and display **additional forms** (non-default varieties) with their images/types
- 🗃️ Uses a local **SQLite** database for fast queries

---

## Tech Stack

- Python
- Streamlit
- SQLite
- Pandas
- Requests (PokeAPI)
- tqdm (progress bar for fetching)

---

## Project Structure

```
pokemon-finder/
├─ Home.py                     # Streamlit app entrypoint
├─ requirements.txt
├─ scripts/
│  ├─ fetch_info.py            # Fetches Pokémon info + forms from PokeAPI -> CSV
│  ├─ fetch_regions.py         # Builds Pokémon-region mapping -> CSV
│  └─ build_db.py              # Merges CSVs and writes SQLite database
├─ utils/
│  └─ utils.py                 # SQLite helper (run_query)
└─ data/
   ├─ regions/                 # Region lists (IDs per region)
   ├─ raw/                     # CSV outputs created by scripts
   └─ processed/               # SQLite database (pokemon.db)
```

---

## Setup

### 1) Create and activate a virtual environment

**macOS / Linux**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```


### 2) Install dependecies
```bash
pip install -r requirements.txt
```

---

## Run the app

From the project root:
```bash
streamlit run 🏠​_Home.py
```
Then open the local URL shown in the terminal (usually http://localhost:8501).

---

## Data Pipeline (Rebuild the Database)
The repository already contains pokemon.db so the app works immediately after cloning.

However, you can rebuild everything from scratch.

### 1) Fetch Pokémon data
```bash
python scripts/fetch_info.py
```
Generates:
data/raw/pokemon_info.csv

### 2) Build region mapping
```bash
python scripts/fetch_regions.py
```
Generates:
data/raw/pokemon_regions.csv

### 3) Build SQLite database
```bash
python scripts/build_db.py
```
Generates:
data/processed/pokemon.db

---

## How it works

1) Data is fetched from PokeAPI.

2) CSV datasets are created.

3) CSV files are merged into a SQLite database.

4) Streamlit queries the database.

5) Results are displayed dynamically with images and filters.

6) Type filtering includes both:

    - main Pokémon types

    - types coming from additional regional forms.

---

## License/Disclaimer

This is a personal educational project.

Pokémon names and related content belong to their respective owners. Data is obtained from public APIs and community resources.