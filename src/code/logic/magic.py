import csv
import textwrap
from logic.scroll import Scroll


class Magic:
    items = []

    @classmethod
    def load_magic_from_csv(cls, filepath):
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            cls.items = []
            for row in reader:
                cls.items.append({
                    "type": row["Type"],
                    "name": row["Name"],
                    "effect": row["Effect"],
                    "cost": row["Cost"],
                    "lore": row.get("Lore", "No lore available."),
                    "lore2": row.get("Lore2", "Ancient secrets remain untold.")
                })

    @classmethod
    def generate_scrolls(cls):
        scrolls = []
        for item in cls.items:
            if item["type"].lower() in ["spell", "enchantment"]:
                scroll = Scroll(name=item["name"], effect=item["effect"], lore=item.get("lore", "No lore available."), cost=int(item["cost"]))
                scrolls.append(scroll)
        return scrolls

    @staticmethod
    def format_magic_info(magic):
        name_and_effect = f'{magic["name"]} - {magic["effect"]} ({magic["cost"]})\n'
        lore = f'"{magic["lore"]}"\n'
        lore2 = f'"{magic["lore2"]}"\n'
        wrapped_lore_lines = textwrap.wrap(lore, width=50)
        wrapped_lore2_lines = textwrap.wrap(lore2, width=50)
        centered_lore_lines = [line.center(50) for line in wrapped_lore_lines]
        centered_lore2_lines = [line.center(50) for line in wrapped_lore2_lines]
        centered_lore = "\n".join(centered_lore_lines)
        centered_lore2 = "\n".join(centered_lore2_lines)
        info = f"{name_and_effect}\n{centered_lore}\n{centered_lore2}"
        return info