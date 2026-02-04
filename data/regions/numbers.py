with open("d:\\pokemon-finder\\data\\regions\\unova.txt", "r", encoding="utf-8") as file:
    for line in file:
        parts = line.strip().split("\t")
        if len(parts) >= 2:
            # Prende il secondo campo, cerca '#' e prende solo ciò che c'è dopo
            number = parts[1].split("#")[-1]  
            print(number.lstrip("0"))  # rimuove eventuali zeri iniziali

