import streamlit as st
import json
import ast

from utils.utils import run_query

st.set_page_config(
    page_title="Pokemon Finder",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Type -> Label + emoji
type_emojis = {
    "": "",
    "normal": "Normal ⚪", "fire": "Fire 🔥", "water": "Water 💧",
    "grass": "Grass 🌿", "electric": "Electric ⚡", "ice": "Ice ❄️",
    "fighting": "Fighting 🥊", "poison": "Poison ☠️", "ground": "Ground 🏔️",
    "flying": "Flying 🕊️", "psychic": "Psychic 🔮", "bug": "Bug 🐛",
    "rock": "Rock 🪨", "ghost": "Ghost 👻", "dark": "Dark 🌑",
    "dragon": "Dragon 🐉", "steel": "Steel ⚙️", "fairy": "Fairy 🧚"
}


def format_types(types_str: str) -> str:
    """
    Format types coming as a comma-separated string (e.g. 'grass, poison')
    into 'Grass 🌿, Poison ☠️'
    """
    if not types_str:
        return ""
    types = [t.strip().lower() for t in str(types_str).split(",") if t.strip()]
    formatted = [type_emojis.get(t, t.capitalize()) for t in types]
    return ", ".join(formatted)


def format_types_from_string(types_str: str) -> str:
    """
    Format types that may come as a Python-list-like string (e.g. "['grass','poison']")
    or as a simple comma-separated string.
    """
    if types_str is None:
        return ""
    try:
        parsed = ast.literal_eval(types_str)
        if isinstance(parsed, list):
            formatted = [type_emojis.get(str(t).lower(), str(t).capitalize()) for t in parsed]
            return ", ".join(formatted)
    except Exception:
        pass

    # fallback: treat as comma-separated
    return format_types(types_str)


def parse_types(types_str: str) -> list[str]:
    """
    Convert the DB value in Types field into a real list of lowercase type strings.
    Accepts either "['grass','poison']" or "grass, poison".
    """
    if types_str is None:
        return []

    try:
        s = str(types_str).strip()
        if s.startswith("["):
            types = ast.literal_eval(s)
        else:
            types = s.split(",")
    except Exception:
        types = str(types_str).split(",")

    return [str(t).strip().lower() for t in types if str(t).strip()]


def has_type(row, tipo_lower: str) -> bool:
    """
    Returns True if the Pokémon has the searched type either in main types or in any extra forms.
    """
    main_types = parse_types(row.get("Types", ""))

    regional_types = []
    regional_forms_val = row.get("RegionalForms")
    if regional_forms_val:
        try:
            forms = json.loads(regional_forms_val) if isinstance(regional_forms_val, str) else regional_forms_val
            for form in forms:
                regional_types.extend([t.strip().lower() for t in form.get("types", [])])
        except Exception:
            pass

    all_types = main_types + regional_types
    return tipo_lower in all_types


@st.cache_data(show_spinner=False)
def get_data(query: str, params: list):
    """Cached DB query to avoid re-querying on every Streamlit rerun."""
    return run_query(query, params)


st.title(":red[Pokémon Finder]")
st.write("Search a Pokémon by name, type or region and view images and external links.")

# --- FILTERS ---
name = st.text_input("Pokémon name (partial allowed):", "Pikachu")

types_list = [""] + [type_emojis[t] for t in type_emojis if t != ""]
tipo_selected = st.selectbox("Type:", types_list)
tipo_lower = "" if tipo_selected == "" else tipo_selected.split(" ")[0].lower()

region_list = ["", "Kanto", "Johto", "Hoenn", "Sinnoh", "Unova",
               "Kalos", "Alola", "Galar", "Paldea"]
region = st.selectbox("Region:", region_list)

if not name and tipo_selected == "" and region == "":
    name = "Pikachu"

# --- BUILD QUERY ---
query = "SELECT * FROM pokemon WHERE 1=1"
params = []

if name:
    query += " AND Name LIKE ?"
    params.append(f"%{name}%")

if region:
    query += " AND Regions LIKE ?"
    params.append(f"%{region.capitalize()}%")

# --- RUN QUERY (CACHED) ---
df = get_data(query, params)

# --- TYPE FILTER IN PYTHON (includes forms types) ---
if tipo_lower and not df.empty:
    df = df[df.apply(lambda row: has_type(row, tipo_lower), axis=1)]

# --- ORDER RESULTS ---
if not df.empty and "Name" in df.columns:
    df = df.sort_values("Name")

st.caption(f"Results found: {len(df)}")

# --- SHOW RESULTS ---
if df.empty:
    st.warning("No Pokémon found with these filters.")
else:
    for _, row in df.iterrows():
        # NOTE: removed vertical_alignment for compatibility with older Streamlit versions
        col1, col2 = st.columns([1, 3])

        with col1:
            image_url = row.get("ImageURL")
            if image_url:
                st.image(image_url, width=120)

        with col2:
            st.markdown(f"### {row.get('Name', '')}")
            st.write(f"**Type:** {format_types_from_string(row.get('Types', ''))}")
            st.write(f"**Regions:** {row.get('Regions', '')}")

            if row.get("HasRegionalForms"):
                st.warning("⚠️ This Pokémon has regional forms / mega evolutions / variants!")

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
                        st.write(f"**{form_name}** — Type: {format_types(form_types)}")

            link = row.get("Link")
            if link:
                st.markdown(f"[Open Bulbapedia page]({link})")

        st.markdown("---")
