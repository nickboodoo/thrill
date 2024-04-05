import csv
import random
import textwrap
from logic.character import Character
from screens.game_screen_parent import GameScreen


class Enemy(Character):
    enemies = []

    @classmethod
    def load_enemies_from_csv(cls, filepath):
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            cls.enemies = []
            for row in reader:
                cls.enemies.append({
                    "name": row["name"], 
                    "health": int(row["health"]), 
                    "attack": int(row["attack"]),
                    "lore": row.get("lore", "Lore not available.")
                })

    @staticmethod
    def generate_random_enemy():
        if not Enemy.enemies:
            Enemy.load_enemies_from_csv('src/data/enemies.csv')
        enemy_info = random.choice(Enemy.enemies)
        return Enemy(enemy_info["name"], enemy_info["health"], enemy_info["attack"])

    @staticmethod
    def format_enemy_info(enemy):
        name_and_stats = f'{enemy["name"]} ({enemy["health"]} HP, {enemy["attack"]} Attack):\n'
        lore = f'"{enemy["lore"]}"'
        wrapped_lore_lines = textwrap.wrap(lore, width=GameScreen.LORE_TEXT_WIDTH)
        centered_lore_lines = [line.center(GameScreen.LORE_TEXT_WIDTH) for line in wrapped_lore_lines]
        centered_lore = "\n".join(centered_lore_lines)
        info = f"{name_and_stats}\n{centered_lore}"
        return info