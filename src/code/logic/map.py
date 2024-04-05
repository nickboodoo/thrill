import csv
import random
from logic.enemy import Enemy
from logic.location import Location


class Map:
    def __init__(self, size, locations_csv_path='src/data/locations.csv'):
        self.nodes = [Location("Soulink Shrine", generate_content_flag=False)]  # Changed here
        location_names = self.load_location_names(locations_csv_path)
        random.shuffle(location_names)
        extended_location_names = (location_names * ((size // len(location_names)) + 1))[:size-1]
        # Use `generate_content_flag=True` for the rest of the locations to potentially generate enemies or vendors
        self.nodes += [Location(name, generate_content_flag=True) for name in extended_location_names]
        
        self.generate_graph()
        self.ensure_at_least_one_enemy()

    def load_location_names(self, csv_path):
        names = []
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                names.append(row['Location'])
        return names

    def generate_graph(self):
        for i in range(len(self.nodes) - 1):
            self.nodes[i].connect(self.nodes[i + 1])
            if i > 0 and random.choice([True, False]):
                self.nodes[i].connect(random.choice(self.nodes[:i]))

    def ensure_at_least_one_enemy(self):
        # Check if any location has an Enemy as its content
        if not any(isinstance(node.content, Enemy) for node in self.nodes):
            # If no location has an Enemy, randomly choose a non-starting location to add an Enemy to
            chosen_location = random.choice(self.nodes[1:])
            chosen_location.content = Enemy.generate_random_enemy()