import requests
import pandas as pd
from tqdm import tqdm
import json

def fetch_info(limit=1010):
    sess = requests.Session()
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"
    resp = sess.get(url).json()
    results = []

    for entry in tqdm(resp["results"], desc="Fetching Info"):
        poke_resp = sess.get(entry["url"]).json()

        poke_id = poke_resp["id"]
        raw_name = poke_resp["name"]

        # --- Normalizzazione del nome principale ---
        species_name = raw_name.split("-")[0]  # parte base prima del trattino
        suffix = raw_name.replace(species_name, "").replace("-", " ").strip()

        if suffix:
            name = f"{species_name.capitalize()} {suffix.title()}"
        else:
            name = species_name.capitalize()

        # --- Tipi ordinati per slot (tipo1, tipo2) ---
        types = [t["type"]["name"] for t in sorted(poke_resp.get("types", []), key=lambda x: x.get("slot", 0))]

        # --- Immagine principale ---
        image_url = poke_resp["sprites"].get("front_default")

        # --- Link Bulbapedia solo col nome base ---
        link = f"https://bulbapedia.bulbagarden.net/wiki/{species_name.capitalize()}_(Pokémon)"

        # --- Estrazione di tutte le forme (regioni, megaevo, ecc.) ---
        species_url = poke_resp["species"]["url"]
        species_data = sess.get(species_url).json()
        varieties = species_data.get("varieties", [])

        regional_forms = []
        for var in varieties:
            if not var.get("is_default", False):
                var_resp = sess.get(var["pokemon"]["url"]).json()
                var_raw_name = var_resp["name"]
                var_name = var_raw_name.replace("-", " ").title()
                r_types = [t["type"]["name"] for t in sorted(var_resp.get("types", []), key=lambda x: x.get("slot", 0))]
                r_image = var_resp["sprites"].get("front_default")

                # fallback se l'immagine standard manca
                if not r_image:
                    other_sprites = var_resp["sprites"].get("other", {})
                    r_image = (
                        other_sprites.get("official-artwork", {}).get("front_default")
                        or other_sprites.get("home", {}).get("front_default")
                    )

                regional_forms.append({
                    "name": var_name,
                    "types": r_types,
                    "image": r_image
                })

        results.append({
            "ID": poke_id,
            "Name": name,
            "BaseName": species_name.capitalize(),  # utile per link o ricerche
            "Types": types,
            "ImageURL": image_url,
            "RegionalForms": json.dumps(regional_forms, ensure_ascii=False),
            "Link": link,
            "HasRegionalForms": bool(regional_forms)
        })

    return pd.DataFrame(results)


if __name__ == "__main__":
    df = fetch_info(limit=1030)
    df.to_csv("data/raw/pokemon_info.csv", index=False)
    print("✅ Saved data/raw/pokemon_info.csv")
