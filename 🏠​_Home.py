import streamlit as st
from utils.utils import run_query
import json
import ast

st.set_page_config(
    page_title="Pokemon Finder",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Dizionario tipi -> Maiuscola + emoji
type_emojis = {
    "": "",
    "normal": "Normal ⚪", "fire": "Fire 🔥", "water": "Water 💧",
    "grass": "Grass 🌿", "electric": "Electric ⚡", "ice": "Ice ❄️",
    "fighting": "Fighting 🥊", "poison": "Poison ☠️", "ground": "Ground 🏔️​",
    "flying": "Flying 🕊️", "psychic": "Psychic 🔮", "bug": "Bug 🐛",
    "rock": "Rock 🪨", "ghost": "Ghost 👻", "dark": "Dark 🌑",
    "dragon": "Dragon 🐉", "steel": "Steel ⚙️", "fairy": "Fairy 🧚"
}

# Funzione per formattare i tipi di un Pokémon
def format_types(types_str):
    types = [t.strip().lower() for t in types_str.split(",") if t.strip()]
    formatted = [type_emojis.get(t, t.capitalize()) for t in types]
    return ", ".join(formatted)

def format_types_from_string(types_str):
    try:
        # Converte la stringa in lista Python
        types_list = ast.literal_eval(types_str)
        # Mappa ogni tipo -> emoji
        formatted = [type_emojis.get(t.lower(), t.capitalize()) for t in types_list]
        return ", ".join(formatted)
    except Exception:
        return types_str   # fallback se non è in quel formato
import ast

# Converte in lista vera se è una stringa tipo "['grass', 'poison']"
def parse_types(types_str):
    try:
        types = ast.literal_eval(types_str) if types_str.startswith("[") else types_str.split(",")
    except:
        types = types_str.split(",")
    return [t.strip().lower() for t in types]

# Funzione per verificare se il Pokémon ha il tipo cercato
def has_type(row, tipo_lower):
    main_types = parse_types(row['Types'])
    regional_types = []
    if row.get("RegionalForms"):
        try:
            forms = json.loads(row["RegionalForms"]) if isinstance(row["RegionalForms"], str) else row["RegionalForms"]
            for form in forms:
                regional_types.extend([t.strip().lower() for t in form.get("types", [])])
        except Exception:
            pass
    all_types = main_types + regional_types
    return tipo_lower in all_types

st.title(":red[Pokémon Finder]")
st.write("Cerca un Pokémon per nome, tipo o regione e visualizza immagini e link esterni.")

# --- INPUT FILTRI ---
name = st.text_input("Nome Pokémon (anche parziale):", "Pikachu")

# Lista tipi con emoji per la selectbox
types_list = [""] + [type_emojis[t] for t in type_emojis if t != ""]
tipo_selected = st.selectbox("Tipo:", types_list)
tipo_lower = "" if tipo_selected == "" else tipo_selected.split(" ")[0].lower()

# Regioni disponibili
region_list = ["","Kanto", "Johto", "Hoenn", "Sinnoh", "Unova",
    "Kalos", "Alola", "Galar", "Paldea"]
region = st.selectbox("Regione:", region_list)

if not name and tipo_selected == "" and region == "":
    name = "Pikachu"

# --- COSTRUZIONE QUERY DINAMICA ---
query = "SELECT * FROM pokemon WHERE 1=1"
params = []

if name:
    query += " AND Name LIKE ?"
    params.append(f"%{name}%")

if region:
    query += " AND Regions LIKE ?"
    params.append(f"%{region.capitalize()}%")

# --- ESECUZIONE QUERY ---
df = run_query(query, params)

# --- FILTRO SUI TIPI LATO PYTHON ---
if tipo_lower:
    df = df[df.apply(lambda row: has_type(row, tipo_lower), axis=1)]

# --- VISUALIZZAZIONE RISULTATI ---
if df.empty:
    st.warning("Nessun Pokémon trovato con questi filtri.")
else:
    for _, row in df.iterrows():
        st.image(row["ImageURL"], width=120)
        st.markdown(f"### {row['Name']}")
        st.write(f"**Tipo:** {format_types_from_string(row["Types"])}")
        st.write(f"**Regioni:** {row['Regions']}")

        if row.get("HasRegionalForms"):
            st.warning("⚠️ Questo Pokémon possiede forme regionali, megaevoluzioni o altre forme!")

            regional_forms = row.get("RegionalForms")
            if regional_forms:
                try:
                    forms = json.loads(regional_forms) if isinstance(regional_forms, str) else regional_forms
                except Exception:
                    forms = []

                for form in forms:
                    form_name = form.get("name", "").title()
                    form_types = ", ".join(form.get("types", []))
                    form_image = form.get("image")

                    if form_image:
                        st.image(form_image, width=120)
                    st.write(f"**{form_name}** — Tipo: {format_types(form_types)}")

        st.markdown(f"[Scheda completa su Bulbapedia]({row['Link']})")
        st.markdown("---")
