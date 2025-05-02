# Hover Revolt of Gamers - Stats Calculator

A Python application with a graphical interface (Tkinter) that lets you **calculate final character stats** in *Hover: Revolt of Gamers*, based on the **chips** equipped, their **quality**, and potential **combo/boosted bonuses**.

---

## Features

- Select any character from the game
- Choose up to **10 individual chips**
- Add **2 groups of combined chips** (bonus if all chips are of the same type)
- Define a **boosted chip** (1.5x multiplier)
- Automatically calculate final stats
- Export and auto-load the last configuration
- Simple and intuitive GUI

---

## Requirements

- **Python 3.7 or later**
- The following standard libraries:
  - `tkinter` (GUI library — may be missing on some installs like Windows Store Python)
  - `json`
  - `collections`
  - `os`, `sys`

> `tkinter` is included by default with most Python distributions.  
> If it's missing, install it via your package manager:

---

## Project Structure

```
project/
│
├── characters.json               # Base stats for characters
├── data.json                     # Chip data and diminishing returns
├── export_chip_config.json       # (Auto-generated) last saved configuration
├── main.py                       # Main script (if using source)
└── README.md                     # This file
```

---

## How to Run

### Option 1: Using the Executable (Recommended for Windows Users)

[Click here to download the executable](https://github.com/DrDJ3006/Hover_Revolt_Of_Gamers_Stats_Calculator/releases/download/v1.0.0/Hover_Revolt_Of_Gamers_Stats_Calculator.exe)

Then simply double-click `Hover_Revolt_Of_Gamers_Stats_Calculator.exe` to launch the app.

No installation required — everything is included.

### Option 2: Using Python (For all OS)

```bash
python main.py
```

---

## JSON Data Format

### Example `characters.json`

```json
{
  "anon_gamer": {
    "acceleration": 20,
    "speed": 20,
    "jump": 20,
      ...
  }
  "greendy": {
    "acceleration": 35,
    "speed": 20,
    "jump": 40,
      ...
  }
}
```

### Example `data.json`

```json
{
  "chip_effects": {
    "ionic_thruster": {
      "acceleration": 0.5,
      "speed": 1
    },
    ....
    "electro_atomic_motor": {
      "acceleration": 0.5,
      "bump_force": 1,
      "bump_resistance": 1,
      ...
    },
  },
  "diminishing_bonus": {
      "ultimate": [10, 8.7, ...],
      "mystic": [9, 7.8, ...],
      "freezing": [8, 7, ...],
  }
}
```

> The `diminishing_bonus` values define how chip effectiveness decreases as you stack the same chip type multiple times.

---

## Export Feature

Each time you export, the build is saved in `export_chip_config.json`, which is automatically reloaded the next time you start the app.

---

## License

Open-source project — free to use for personal or educational purposes.
