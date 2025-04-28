
# Données issues du tableau de qualités de chips
chip_qualities = {
    "Cheap": 4.5,
    "Broken": 5.0,
    "Basic": 5.5,
    "Quality": 6.0,
    "Dirty": 6.5,
    "High Tech": 7.0,
    "Glowing": 7.5,
    "Freezing": 8.0,
    "Crystal": 8.5,
    "Mystic": 9.0,
    "Royal": 9.5,
    "Ultimate": 10.0
}
# Données issues du tableau d'effets des chips
chip_effects = {
    "Ionic Thruster": {
        "Acceleration": 5,
        "Speed": 10
    },
    "Pulse Generator": {
        "Jump": 10,
        "Bounciness": 10
    },
    "Magnetic Dynamo": {
        "Grind Speed": 10,
        "Slide Speed": 10,
        "Energy": 10
    },
    "Electro-Atomic Motor": {
        "Acceleration": 5,
        "Bump Force": 10,
        "Bump Resistance" : 10,
        "Ball Handling": 10
    },
    "Hacking Processor": {
        "Stealth": 10,
        "Hacking": 10,
        "Hoverheat": 10
    }
}
# Création du tableau 
diminishing_bonus = {
    "Ultimate": [10, 8.7, 7.7, 6.9, 6.2, 5.7, 5.3, 4.9, 4.5, 4.3, 4, 3.8, 3.6, 3.4, 3.2],
    "Mystic": [9, 7.8, 6.9, 6.2, 5.6, 5.1, 4.7, 4.4, 4.1, 3.8, 3.6, 3.4, 3.2, 3.1, 2.9],
    "Freezing": [8, 7, 6.2, 5.5, 5, 4.6, 4.2, 3.9, 3.6, 3.4, 3.2, 3, 2.9, 2.7, 2.6],
    "High Tech": [7, 6.1, 5.4, 4.8, 4.4, 4, 3.7, 3.4, 3.2, 3, 2.8, 2.6, 2.5, 2.4, 2.3],
    "Quality": [6, 5.2, 4.6, 4.1, 3.7, 3.4, 3.2, 2.9, 2.7, 2.6, 2.4, 2.3, 2.1, 2, 1.9],
    "Broken": [5, 4.3, 3.8, 3.4, 3.1, 2.9, 2.6, 2.4, 2.3, 2.1, 2, 1.9, 1.8, 1.7, 1.6]
}

