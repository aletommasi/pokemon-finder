import pandas as pd
import sqlite3

# Carico CSV generati dai fetch script
df_info = pd.read_csv("data/raw/pokemon_info.csv")          # PokemonID, SpeciesID, Name, Region, Types, ImageURL, Link
df_regions = pd.read_csv("data/raw/pokemon_regions.csv")    # PokemonID, Regions

# Rinomino la colonna per uniformarla
df_regions.rename(columns={"ID_Pokemon": "ID"}, inplace=True)

# Merge usando ID
df = pd.merge(df_info, df_regions, on="ID", how="left")

# Creo/aggiorno il DB SQLite
conn = sqlite3.connect("data/processed/pokemon.db")
df.to_sql("pokemon", conn, if_exists="replace", index=False)
conn.close()

print(f"✅ DB created with {len(df)} rows (including regional forms)")
