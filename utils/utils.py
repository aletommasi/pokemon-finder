# app/utils.py
import sqlite3
import pandas as pd

DB_PATH = "data/processed/pokemon.db"

def run_query(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df
