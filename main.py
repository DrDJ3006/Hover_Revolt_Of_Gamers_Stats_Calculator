import json
from collections import Counter, defaultdict, OrderedDict

# Charger les fichiers JSON
def load_data():
    with open('characters.json', 'r', encoding='utf-8') as f:
        characters_data = json.load(f)
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return characters_data, data

# Fonction pour compter le nombre de chaque type de chip dans un build
def count_chip_types(build):
    type_counter = Counter()

    for chip in build.get("chips", []):
        type_counter[chip["type"]] += 1

    for group in build.get("combined_groups", []):
        for chip in group:
            type_counter[chip["type"]] += 1

    boosted = build.get("boosted_chip")
    if boosted:
        type_counter[boosted["type"]] += 1

    return dict(type_counter)

# Fonction pour calculer les bonus d'un build
def calc_stats(data, build):
    chip_count = count_chip_types(build)
    boosted_chips_bonus = 1.5
    total_bonus = defaultdict(float)

    def apply_chip(chip, multiplier=1.0):
        chip_type = chip['type']
        quality = chip['quality']
        bonus = data['diminishing_bonus'][quality][chip_count[chip_type] - 1]
        chip_effects = data["chip_effects"][chip_type]
        for stat, value in chip_effects.items():
            total_bonus[stat] += value * bonus * multiplier

    for chip in build.get("chips", []):
        apply_chip(chip)

    for group in build.get("combined_groups", []):
        types = {chip["type"] for chip in group}
        multiplier = boosted_chips_bonus if len(types) == 1 else 1.0
        for chip in group:
            apply_chip(chip, multiplier)

    boosted_chip = build.get("boosted_chip")
    if boosted_chip:
        apply_chip(boosted_chip, boosted_chips_bonus)

    return {stat: round(value) for stat, value in total_bonus.items()}

# Fonction principale
def main():
    # Charger les données
    characters_data, data = load_data()

    # Définir le build
    build = {
        "chips": [
            {"type": "ionic_thruster", "quality": "ultimate"},
            {"type": "pulse_generator", "quality": "ultimate"},
            {"type": "hacking_processor", "quality": "ultimate"},
            {"type": "hacking_processor", "quality": "ultimate"},
            {"type": "hacking_processor", "quality": "ultimate"},
            {"type": "hacking_processor", "quality": "ultimate"},
            {"type": "hacking_processor", "quality": "ultimate"},
            {"type": "hacking_processor", "quality": "ultimate"},
            {"type": "hacking_processor", "quality": "ultimate"},
            {"type": "hacking_processor", "quality": "ultimate"},
        ],
        "combined_groups": [
            [
                {"type": "ionic_thruster", "quality": "ultimate"},
                {"type": "ionic_thruster", "quality": "ultimate"}
            ],
            [
                {"type": "pulse_generator", "quality": "ultimate"},
                {"type": "pulse_generator", "quality": "ultimate"}
            ]
        ],
        "magnetic_dynamo": {
            "type": "ionic_thruster",
            "quality": "ultimate"
        }
    }

    # Sélectionner le personnage
    character = "wattabax"

    # Calculer les bonus
    bonus_stats = calc_stats(data, build)

    # Fusionner les stats du personnage et du build
    final_stats = OrderedDict()

    for key in characters_data[character]:
        final_stats[key] = characters_data[character][key] + bonus_stats.get(key, 0)

    for key in bonus_stats:
        if key not in characters_data[character]:
            final_stats[key] = bonus_stats[key]

    # Convertir en dictionnaire normal pour affichage
    final_stats = dict(final_stats)
    # Afficher le résultat
    for stat, value in final_stats.items():
        print(f"{stat}: {value}")


# Lance main() si on exécute ce fichier
if __name__ == "__main__":
    main()
