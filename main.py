from collections import Counter, OrderedDict, defaultdict
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class App:
    def __init__(self, master, character_names, chip_names, quality_names, data):
        self.master = master
        self.master.title("Hover Revolt Of Gamers Stats Calculator")
        self.master.geometry("600x600")

        self.character_names = character_names
        self.chip_names = chip_names
        self.quality_names = quality_names
        self.data = data

        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(side="top", fill="x")
        self.top_frame.grid_propagate(False)

        self.left_frame = tk.Frame(self.top_frame)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5))

        self.right_frame = tk.Frame(self.top_frame)
        self.right_frame.pack(side="left", fill="both", expand=True, padx=(5, 10))

        self.bottom_frame = tk.Frame(self.master)
        self.bottom_frame.pack(side="top", fill="both", expand=True, pady=(10, 5))

        self.build_left_frame()
        self.build_right_frame()

        button_frame = tk.Frame(self.right_frame)
        button_frame.pack(pady=10)

        self.export_button = ttk.Button(button_frame, text="Export", command=self.export_build)
        self.export_button.pack(side="left", padx=5)

        self.calc_button = ttk.Button(button_frame, text="Calculate Stats", command=self.calc_build)
        self.calc_button.pack(side="left", padx=5)

        self.build_bottom_frame()

        try:
            with open("export_chip_config.json", "r") as f:
                saved_build = json.load(f)
            self.load_build(saved_build)
        except FileNotFoundError:
            self.stats_text.insert("end", "Last export file not found\n")
            self.stats_text.config(state="disabled")

    def create_chip_quality_row(self, parent):
        chip_var = tk.StringVar()
        chip = ttk.Combobox(parent, width=17, state="readonly", textvariable=chip_var, values=self.chip_names)
        chip.pack(side="left", padx=2)
        quality_var = tk.StringVar()
        quality = ttk.Combobox(parent, width=17, state="readonly", textvariable=quality_var, values=self.quality_names)
        quality.pack(side="left", padx=2)
        return chip_var, quality_var

    def build_left_frame(self):
        self.chip_quality_vars = []

        tk.Label(self.left_frame, text="Character").pack(pady=(10, 0))
        self.character_var = tk.StringVar()
        self.character_dropdown = ttk.Combobox(self.left_frame, textvariable=self.character_var, state="readonly", width=36, values=self.character_names)
        self.character_dropdown.pack(pady=5)

        title_frame = tk.Frame(self.left_frame)
        title_frame.pack(pady=(10, 2))
        tk.Label(title_frame, text="Chip", width=17, anchor="w").pack(side="left", padx=2)
        tk.Label(title_frame, text="Quality", width=17, anchor="w").pack(side="left", padx=2)

        for _ in range(10):
            row = tk.Frame(self.left_frame)
            row.pack(pady=2)
            chip_var, quality_var = self.create_chip_quality_row(row)
            self.chip_quality_vars.append((chip_var, quality_var))

    def build_right_frame(self):
        self.combined_vars_1 = []
        self.combined_vars_2 = []

        tk.Label(self.right_frame, text="Combined Chips (1)").pack(pady=(15, 5))
        for _ in range(2):
            row = tk.Frame(self.right_frame)
            row.pack(pady=2)
            chip_var, quality_var = self.create_chip_quality_row(row)
            self.combined_vars_1.append((chip_var, quality_var))

        tk.Label(self.right_frame, text="Combined Chips (2)").pack(pady=(15, 5))
        for _ in range(2):
            row = tk.Frame(self.right_frame)
            row.pack(pady=2)
            chip_var, quality_var = self.create_chip_quality_row(row)
            self.combined_vars_2.append((chip_var, quality_var))

        tk.Label(self.right_frame, text="Boosted Chip").pack(pady=(15, 5))
        row = tk.Frame(self.right_frame)
        row.pack(pady=2)
        self.boosted_vars = self.create_chip_quality_row(row)

    def build_bottom_frame(self):
        self.stats_text = tk.Text(self.bottom_frame, height=6, wrap="word", font=("Courier", 10), bg="#f7f7f7", relief="sunken", borderwidth=1)
        self.stats_text.pack(fill="both", expand=True, padx=10, pady=5)
        self.stats_text.config(state="disabled")

    def export_build(self):
        result = self.get_build()
        with open("export_chip_config.json", "w") as f:
            json.dump(result, f, indent=2)
        self.stats_text.config(state="normal")
        self.stats_text.insert("end", "Configuration exported to export_chip_config.json\n")
        self.stats_text.config(state="disabled")

    def get_build(self):
        result = {
            "character": self.character_var.get(),
            "chips": [],
            "combined_groups": [],
            "boosted_chip": {
                "type": self.boosted_vars[0].get(),
                "quality": self.boosted_vars[1].get()
            }
        }

        for chip_var, quality_var in self.chip_quality_vars:
            result["chips"].append({"type": chip_var.get(), "quality": quality_var.get()})

        for group_vars in [self.combined_vars_1, self.combined_vars_2]:
            group = []
            for chip_var, quality_var in group_vars:
                group.append({"type": chip_var.get(), "quality": quality_var.get()})
            result["combined_groups"].append(group)

        return result

    def calc_build(self):
        build = self.get_build()
        if not build["character"]:
            self.stats_text.config(state="normal")
            self.stats_text.delete("1.0", tk.END)
            self.stats_text.insert("end", "Please select a character.\n")
            self.stats_text.config(state="disabled")
            return

        bonus_stats = calc_stats(self.data, build)
        character = build["character"]

        if character in characters_data:
            base_stats = characters_data[character]
            final_stats = OrderedDict()

            # Ajouter les stats de base dans l'ordre défini
            for key in base_stats:
                final_stats[key] = base_stats[key] + bonus_stats.get(key, 0)

            # Ajouter les stats bonus qui ne sont pas dans les stats de base
            for key in bonus_stats:
                if key not in final_stats:
                    final_stats[key] = bonus_stats[key]

            self.stats_text.config(state="normal")
            self.stats_text.delete("1.0", tk.END)
            self.stats_text.insert(tk.END, "=== FINAL STATS ===\n")
            for stat, value in final_stats.items():
                self.stats_text.insert(tk.END, f"{stat}: {value}\n")
            self.stats_text.config(state="disabled")
        else:
            self.stats_text.config(state="normal")
            self.stats_text.delete("1.0", tk.END)
            self.stats_text.insert("end", f"Character '{character}' not found.\n")
            self.stats_text.config(state="disabled")

    def load_build(self, build):
        self.character_var.set(build.get("character", ""))

        for (chip_var, quality_var), chip_data in zip(self.chip_quality_vars, build.get("chips", [])):
            chip_var.set(chip_data.get("type", ""))
            quality_var.set(chip_data.get("quality", ""))

        for group_vars, group_data in zip([self.combined_vars_1, self.combined_vars_2], build.get("combined_groups", [])):
            for (chip_var, quality_var), chip_data in zip(group_vars, group_data):
                chip_var.set(chip_data.get("type", ""))
                quality_var.set(chip_data.get("quality", ""))

        boosted = build.get("boosted_chip", {})
        self.boosted_vars[0].set(boosted.get("type", ""))
        self.boosted_vars[1].set(boosted.get("quality", ""))

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

def calc_stats(data, build):
    chip_count = count_chip_types(build)
    boosted_chips_bonus = 1.5
    total_bonus = defaultdict(float)

    def apply_chip(chip, multiplier=1.0):
        chip_type = chip.get('type', '')
        quality = chip.get('quality', '')
        if not chip_type or not quality:
            messagebox.showwarning("Incomplete Chips", "Some chips had missing type or quality and were ignored.")
            return
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

if __name__ == "__main__":
    with open("./characters.json", "r") as f:
        characters_data = json.load(f)

    with open("./data.json", "r") as f:
        chip_data = json.load(f)

    character_names = list(characters_data.keys())
    chip_names = list(chip_data["chip_effects"].keys())
    quality_names = list(chip_data["diminishing_bonus"].keys())

    root = tk.Tk()
    app = App(root, character_names, chip_names, quality_names, chip_data)
    root.mainloop()
