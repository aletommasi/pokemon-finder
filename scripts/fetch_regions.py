import csv

# dizionario globale
pokemon_dict = {}

def fetch_regions(file_path, region_name, pokemon_dict):
    """
    Apre un file contenente ID Pokémon, rimuove gli zeri iniziali e aggiorna il dizionario globale pokemon_dict.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            poke_id = line.strip().lstrip("0")
            if poke_id:
                if poke_id not in pokemon_dict:
                    pokemon_dict[poke_id] = []
                pokemon_dict[poke_id].append(region_name)

def save_to_csv(output_file, pokemon_dict):
    """
    Salva il dizionario pokemon_dict in CSV.
    """
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID_Pokemon", "Regions"])
        for poke_id, regions in sorted(pokemon_dict.items(), key=lambda x: int(x[0])):
            writer.writerow([poke_id, ",".join(regions)])


fetch_regions("data\\regions\\kanto.txt", "Kanto", pokemon_dict)
fetch_regions("data\\regions\\johto.txt", "Johto", pokemon_dict)
fetch_regions("data\\regions\\hoenn.txt", "Hoenn", pokemon_dict)
fetch_regions("data\\regions\\sinnoh.txt", "Sinnoh", pokemon_dict)
fetch_regions("data\\regions\\unova.txt", "Unova", pokemon_dict)
fetch_regions("data\\regions\\kalos.txt", "Kalos", pokemon_dict)
fetch_regions("data\\regions\\alola.txt", "Alola", pokemon_dict)
fetch_regions("data\\regions\\galar.txt", "Galar", pokemon_dict)
fetch_regions("data\\regions\\paldea.txt", "Paldea", pokemon_dict)

save_to_csv("data\\raw\\pokemon_regions.csv", pokemon_dict)
